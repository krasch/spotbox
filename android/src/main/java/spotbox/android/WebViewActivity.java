package spotbox.android;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.util.Log;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;

import java.net.URI;
import java.net.URISyntaxException;


public class WebViewActivity extends Activity {

        private WebView webView;
        private WebSocketClient mWebSocketClient;

        public void onCreate(Bundle savedInstanceState) {

                super.onCreate(savedInstanceState);

                //connectWebSocket();

                setContentView(R.layout.webview);

                webView = (WebView) findViewById(R.id.webview);
                webView.setWebViewClient(new WebViewClient());
                webView.getSettings().setJavaScriptEnabled(true);

                // map console logger to adb logger
                webView.addJavascriptInterface(new ConsoleLogger(this), "logger");
                webView.loadUrl("javascript:console={};console.log = function(msg) {logger.onConsoleMessage(msg);};");

                webView.loadUrl("http://192.168.1.121:8080/test.html");

        }

        private void connectWebSocket() {
            URI uri;
            try {
                uri = new URI("ws://192.168.0.11:8080/ws");
            } catch (URISyntaxException e) {
                e.printStackTrace();
                return;
            }

            mWebSocketClient = new WebSocketClient(uri) {
                @Override
                public void onOpen(ServerHandshake serverHandshake) {
                    Log.i("Websocket", "Opened");
                    mWebSocketClient.send("{\"command\": \"add\",\"uri\": \"spotify:track:2uki1VRt9gZs2za2VUoBIC\"}");
                }

                @Override
                public void onMessage(String s) {
                }

                @Override
                public void onClose(int i, String s, boolean b) {
                    Log.i("Websocket", "Closed " + s);
                }

                @Override
                public void onError(Exception e) {
                    Log.i("Websocket", "Error " + e.getMessage());
                }
            };
            mWebSocketClient.connect();
        }
}


