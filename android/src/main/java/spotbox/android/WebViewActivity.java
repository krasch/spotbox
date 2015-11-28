package spotbox.android;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class WebViewActivity extends Activity {

        private WebView webView;

        public void onCreate(Bundle savedInstanceState) {

                super.onCreate(savedInstanceState);

                setContentView(R.layout.webview);

                webView = (WebView) findViewById(R.id.webview);
                webView.setWebViewClient(new WebViewClient());

                webView.getSettings().setJavaScriptEnabled(true);
                webView.addJavascriptInterface(new ConsoleLogger(this), "logger");


                webView.loadUrl("http://192.168.0.11:8080/ws-example.html");

        }
}


