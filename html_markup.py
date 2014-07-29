# http://www.reddit.com/r/dailyprogrammer/comments/289png/6162014_challenge_167_easy_html_markup_generator/

def main():
    f = open('markup.html', 'w')
    f.write('''<!DOCTYPE html>
<html>
    <head>
        <title></title>
    </head>
    <body>
        <p>'''+raw_input('Enter Paragraph Text: ')+'''</p>
    </body>
</html>''')
    f.close()

main()