package spotbox.android;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.util.Log;

import java.net.URI;
import java.net.URISyntaxException;

public class WebViewActivity extends Activity {

        private final String IP = "192.168.1.121";
        private final String PORT = "8080";

        private final String playerURI = "http://"+IP+":"+PORT;
        private final String webSocketURI = "ws://"+IP+":"+PORT+"/ws";

        private WebView webView;
        private SocketBinding socket;

        public void onCreate(Bundle savedInstanceState) {

                super.onCreate(savedInstanceState);
                setContentView(R.layout.webview);

                webView = (WebView) findViewById(R.id.webview);
                webView.getSettings().setJavaScriptEnabled(true);

                socket = new SocketBinding(parseURI(webSocketURI), webView, this);
                webView.addJavascriptInterface(socket, "androidSocket");

                // as soon as website has finished loading, connect the socket
                // would miss initial messages from socket server if connecting before page has loaded

                webView.setWebViewClient(new WebViewClient(){
                      @Override
                      public void onPageFinished(WebView view, String url) {
                          Log.i("spotbox", url);
                          socket.connect();
                      }
                });

                // map console logger to adb logger
                webView.addJavascriptInterface(new ConsoleLogger(this), "logger");
                webView.loadUrl("javascript:console={};console.log = function(msg) {logger.onConsoleMessage(msg);};");

                // load the player
                webView.loadUrl(playerURI);
        }

        private URI parseURI(String uriString) {
            URI webSocketURI = null;
            try {
                 return new URI(uriString);
            }
            catch (URISyntaxException e) {
                 throw new RuntimeException("Bad uri, better die directly");
            }

        }
}


