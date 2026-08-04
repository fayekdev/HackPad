import webbrowser 


class WebsiteAction:

    def execute(self, action):

        if "data" in action:
            url = action["data"].get("url", "")
        else:
            url = action.get("url", "")

        if not url:
            return
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        try:
            webbrowser.open(url)

        except Exception as e:
            print("WebsiteAction Error:", e)