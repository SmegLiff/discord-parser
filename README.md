# Discord Parser
Parses HTML file containing Discord chat logs into CSV.

Made to work with the HTML file exported by https://github.com/Tyrrrz/DiscordChatExporter so it should work.

That thing should be able to render CSV properly on its own but due to a technical issue that was not caused by me I had to do this.

# HTML to CSV
Put input / output directories at the top of htmlparser.py and hope your computer doesn't die/

# CSV to Plaintext
Same as above, should be less painful on your computer.
Change `combineMessages` from `True` to `False` to disable merging multiple messages from the same author with the same timestamp

* Code is extremely awful I made this in one sitting for a private use ok.
