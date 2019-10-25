from flask import redirect, url_for, current_app, render_template, request


def index():
    names = ['Next', 'Prev', 'Reset', 'Btn4', 'Btn5', 'Btn6', 'Btn7']
    if current_app.data['state_num'] is not None:
        try:
            current_app.data['state'] = current_app.settings['states'][current_app.data['state_num']]
        except IndexError:
            print(f'invalid state num: {current_app.data["state_num"]}')
    btns = zip(names, [(b.__name__) for b in btn_functs])
    return render_template('index.html', btns=btns, data=current_app.data, states=current_app.settings['states'])


def web_config():
    if request.method == 'POST':
        for i in range(1, 8):
            current_app.settings['tables'][i] = request.form[f'table{i}']
        print(current_app.settings['tables'])
    return render_template('config.html', config=current_app.settings)


def btn1():
    current_app.data['message'] = 'btn1'
    if current_app.data['state_num'] is None:
        current_app.data['state_num'] = 0
    elif current_app.data['state_num'] < len(current_app.settings['states']) - 1:
        current_app.data['state_num'] += 1
    return redirect(url_for('index'))


def btn2():
    current_app.data['message'] = 'btn2'
    if current_app.data['state_num'] > 0:
        current_app.data['state_num'] -= 1
    return redirect(url_for('index'))


def btn3():
    current_app.data['message'] = 'btn3'
    current_app.data['state_num'] = 0
    return redirect(url_for('index'))


def btn4():
    current_app.data['message'] = 'btn4'
    return redirect(url_for('index'))


def btn5():
    current_app.data['message'] = 'btn5'
    return redirect(url_for('index'))


def btn6():
    current_app.data['message'] = 'btn6'
    return redirect(url_for('index'))


def btn7():
    current_app.data['message'] = 'btn7'
    return redirect(url_for('index'))


# Set up buttons
btn_functs = [btn1, btn2, btn3, btn4, btn5, btn6, btn7]
