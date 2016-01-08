/*
Forwards messages from websocket server to JS frontend and vice versa.
*/

package spotbox.android;

import android.util.Log;
import android.webkit.WebView;
import android.webkit.JavascriptInterface;
import android.content.Context;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import java.net.URI;

public class SocketBinding extends WebSocketClient {

    WebView webView;
    Context context;

    public SocketBinding(URI serverURI, WebView webView, Context context) {
		super(serverURI);
        this.webView = webView;
        this.context = context;
	}

    @Override
    public void onOpen(ServerHandshake serverHandshake) {
        Log.i("spotbox", "Socket opened");
    }

    @Override
    public void onMessage(String s) {
        s = s + " ";
        webView.loadUrl("javascript: socket.onmessage('" + s + "');");
    }

    @Override
    public void onClose(int i, String s, boolean b) {
        Log.i("spotbox", "Socket closed " + s);
    }

    @Override
    public void onError(Exception e) {
        Log.e("spotbox", "Error " + e.getMessage());
    }

    @Override
    public void connect() {
        super.connect();
        webView.loadUrl("javascript:socket.send = function(msg) {androidSocket.onMessageFromJS(msg);};");
    }

    @JavascriptInterface
    public void onMessageFromJS(String message) {
        Log.i("spotbox", "ladida");
        Log.i("spotbox", message);
        send(message);
    }
}