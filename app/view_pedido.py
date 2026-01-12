from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, jsonify
)
from app import db
from app.models import Pedido, ItemPedido, Produto, Usuario

pedido_bp = Blueprint('pedido', __name__)

# =========================
# CHECKOUT
# =========================
@pedido_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'usuario_id' not in session:
        flash("Faça login para continuar", "warning")
        return redirect(url_for('main.login'))

    usuario = Usuario.query.get(session['usuario_id'])
    carrinho = session.get('carrinho', {})

    if not carrinho:
        flash("Carrinho vazio", "warning")
        return redirect(url_for('main.delivery'))

    itens = []
    total = 0

    for produto_id, qtd in carrinho.items():
        produto = Produto.query.get(int(produto_id))
        if produto:
            subtotal = produto.valor_venda * qtd
            total += subtotal
            itens.append({
                'produto': produto,
                'quantidade': qtd,
                'subtotal': subtotal
            })

    if request.method == 'POST':
        forma_pagamento = request.form['forma_pagamento']

        pedido = Pedido(
            usuario_id=usuario.id,
            total=total,
            forma_pagamento=forma_pagamento,
            status='Aguardando pagamento'
        )
        db.session.add(pedido)
        db.session.flush()  # pega ID do pedido

        for item in itens:
            db.session.add(ItemPedido(
                pedido_id=pedido.id,
                produto_nome=item['produto'].nome,
                preco=item['produto'].valor_venda,
                quantidade=item['quantidade'],
                subtotal=item['subtotal']
            ))

        db.session.commit()
        session.pop('carrinho')

        flash("Pedido criado com sucesso!", "success")
        return redirect(url_for('pedido.meus_pedidos'))

    return render_template(
        'checkout.html',
        usuario=usuario,
        itens=itens,
        total=total
    )

# =========================
# HISTÓRICO DE PEDIDOS
# =========================
@pedido_bp.route('/meus-pedidos')
def meus_pedidos():
    if 'usuario_id' not in session:
        flash("Faça login", "warning")
        return redirect(url_for('main.login'))

    pedidos = Pedido.query.filter_by(
        usuario_id=session['usuario_id']
    ).order_by(Pedido.data.desc()).all()

    return render_template(
        'meus_pedidos.html',
        pedidos=pedidos
    )
from flask import Blueprint, render_template, session, redirect, url_for
from app.models import Usuario

main = Blueprint('main', __name__)

@main.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('main.login'))

    usuario = Usuario.query.get(session['usuario_id'])
    return render_template('perfil.html', usuario=usuario)
    