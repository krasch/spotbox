<queue>
    <div each={ item, i in items }>{ item }</div>
    this.items = ["test", "abc", "cde"]

    this.on('update', function(){ console.log("queue loaded")});

    this.on('bla', function(){console.log("bla")});
    /*function bla() {
        console.log("bla");
    }*/
</queue>