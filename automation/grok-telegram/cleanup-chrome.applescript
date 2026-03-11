tell application "Google Chrome"
  if not running then return
  set keepPrefixes to {"https://grok.com/", "https://x.com/", "chrome-extension://"}
  repeat with w in every window
    set closeList to {}
    repeat with t in every tab of w
      set u to URL of t
      set keepTab to false
      repeat with p in keepPrefixes
        if u starts with (contents of p) then
          set keepTab to true
          exit repeat
        end if
      end repeat
      if keepTab is false then set end of closeList to t
    end repeat
    repeat with t in reverse of closeList
      close t
    end repeat
  end repeat
  hide
end tell
