/*
Take javascript logging messages and show them in android log.
Small workaround for bug in some HTC phones that do not forward console log messages.
*/
package spotbox.android;

import android.content.Context;
import android.webkit.JavascriptInterface;
import android.util.Log;

public class ConsoleLogger {
    Context mContext;

    ConsoleLogger(Context c) {
        mContext = c;
    }

    @JavascriptInterface
    public void onConsoleMessage(String message) {
         Log.d("spotbox", message);
    }

}