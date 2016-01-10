<app>
  <queue></queue>

  <script>

    console.log(opts);
    socketUri = "ws://"+window.location.host+"/ws"

    this.on('updated', function(){ console.log("app loaded");     this.tags.queue.trigger("bla");});

    this.tags.queue.trigger("bla");
  </script>
</app>