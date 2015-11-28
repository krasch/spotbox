package spotbox.android;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.ConsoleMessage;
import android.util.Log;

public class WebViewActivity extends Activity {

        private WebView webView;

        public void onCreate(Bundle savedInstanceState) {

                super.onCreate(savedInstanceState);

                setContentView(R.layout.webview);

                webView = (WebView) findViewById(R.id.webview);
                webView.setWebViewClient(new WebViewClient(){
                    public boolean onConsoleMessage(ConsoleMessage cm) {
                        Log.d("spotbox", cm.message() + " -- From line " + cm.lineNumber() + " of " + cm.sourceId() );
                        return true;
                      }});


                webView.getSettings().setJavaScriptEnabled(true);
                webView.loadUrl("http://192.168.1.134:8080");

        }

}


