from flask import Flask, render_template, request

app = Flask(__name__)


def shift_char(char, shift_amount):
    if char.isalpha():
        base = ord('a') if char.islower() else ord('A')
        return chr((ord(char) - base + shift_amount) % 26 + base)
    return char


def process_text(text, shift, mode):
    # decrypt = reverse the shift
    if mode == "decrypt":
        shift = -shift
    return ''.join(shift_char(char, shift) for char in text)


@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    error = ""
    text = ""
    shift = ""
    mode = "encrypt"

    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        shift_raw = request.form.get('shift', '').strip()
        mode = request.form.get('mode', 'encrypt')

        if not text:
            error = "Please enter some text."
        elif not shift_raw.lstrip('-').isdigit():
            error = "Shift value must be a number."
        else:
            shift = int(shift_raw) % 26
            result = process_text(text, shift, mode)

    return render_template('index.html', result=result, error=error,
                           text=text, mode=mode)


if __name__ == '__main__':
    app.run(debug=True)
