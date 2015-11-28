/*
Take javascript logging messages and show them in android log.
Small workaround for bug in some HTC phones that do not forward console log messages.

You need to add 'console.log = logger.onConsoleMessage;' to your javascript code.
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