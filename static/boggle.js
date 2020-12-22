class BoggleGame {

    constructor(boardId, seconds = 60) {
        this.seconds = seconds;
        this.showTimer();

        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);
        this.timer = setInterval(this.sec.bind(this), 1000);

        $('.add-word', this.board).on('submit', this.handleSubmit.bind(this));
    }
    
    wordList(word) {
        $(".words", this.board).append($("<li></li>", { text: word }));
    }

    showScore() {
        $('.score', this.board).text(this.score);
    }

    showMessage(msg, cls) {
        $('.msg', this.board)
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
    }

    showTimer() {
        $('.timer', this.board).text(this.seconds);
    }

    async sec() {
        this.seconds -= 1;
        this.showTimer();

        if (this.seconds === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    async handleSubmit(event) {
        event.preventDefault();
        const $word = $(".word", this.board);

        let word = $word.val();
        if (!word) return;

        if (this.words.has(word)) {
            this.showMessage(`Already found ${word}`);
            return;
        }
    
        const response = await axios.get("/word-check", { params: { word: word } });
        if (response.data.result === 'not-word') {
            this.showMessage(`${word} is not a valid word`);
        } else if (response.data.result === 'not-on-board') {
            this.showMessage(`${word} is not on the board`);
        } else {
            this.wordList(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`${word} added to list`);
        }
        $word.val('').focus();
    }
    async scoreGame() {

        $('.add-word', this.board).hide();
        const response = await axios.post('/show-score', { score: this.score });
        if (response.data.newRecord) {
        this.showMessage(`New Record: ${this.score}`);
        } else {
        this.showMessage(`Final Score: ${this.score}`);
    }
  }
}
