from flask import Flask, redirect, render_template, request, jsonify, session, url_for

app = Flask(__name__)
app.secret_key="secret_key"


# Başlangıç oyun durumunu ayrı fonksiyonda tanımlıyoruz.
def initial_game_state():
    return {
        'zümrüt': 60,
        'yakut': 60,
        'safir': 60,
        'altin': 0,
        'message': 'Oyuna hoş geldin! Bir takas yaparak başla.'
    }

# Oyun durumunu global değişken yapıyoruz.
game_state = initial_game_state()

@app.route("/")
def index():
    return render_template("index.html", game_state=game_state)

@app.route("/restart", methods=["POST"])
def restart():
    global game_state
    # Oyun durumunu sıfırla
    game_state = initial_game_state()
    session.clear()
    return redirect(url_for("index"))

@app.route('/takas', methods=['POST'])
def takas():
    global game_state
    data = request.get_json()
    takas_id = data.get('takas_id')

    if takas_id == 'takas1':
        if game_state['yakut'] >= 1 and game_state['safir'] >= 1:
            game_state['yakut'] -= 1
            game_state['safir'] -= 1
            game_state['zümrüt'] += 1
            game_state['altin'] += 1
            game_state['message'] = 'Takas başarılı! 1 Zümrüt ve 1 Altın kazandınız.'
        else:
            game_state['message'] = 'Geçersiz takas! Yeterli yakut veya safiriniz yok.'

    elif takas_id == 'takas2':
        if game_state['zümrüt'] >= 1 and game_state['safir'] >= 1:
            game_state['zümrüt'] -= 1
            game_state['safir'] -= 1
            game_state['yakut'] += 1
            game_state['altin'] += 1
            game_state['message'] = 'Takas başarılı! 1 Yakut ve 1 Altın kazandınız.'
        else:
            game_state['message'] = 'Geçersiz takas! Yeterli zümrüt veya safiriniz yok.'
            
    elif takas_id == 'takas3':
        if game_state['yakut'] >= 1:
            game_state['yakut'] -= 1
            game_state['safir'] += 2
            game_state['altin'] += 1
            game_state['message'] = 'Takas başarılı! 2 Safir kazandınız.'
        else:
            game_state['message'] = 'Geçersiz takas! Yeterli yakutunuz yok.'
    else:
        game_state['message'] = 'Bilinmeyen takas IDsi.'

    return jsonify(game_state)

if __name__ == '__main__':
    app.run(debug=True)
