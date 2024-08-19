from telethon import TelegramClient
import random
import asyncio
from datetime import datetime, timedelta

# Configurações do API ID, HASH do Telegram e Token do Bot
api_id = 26242551
api_hash = '45b7dfe56dc990540fb60c1bde3b599a'
bot_token = '6648288424:AAEWyVBMnCFpgGH0ATkmIIUyAJ06gRhcpEo'

# ID do grupo para onde você quer enviar os sinais
target_group_id = 4237599851  # Substitua com o ID do grupo desejado

# Inicializa o cliente do Telegram
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

def generate_mines_pattern():
    positions = list(range(25))
    
    num_bombs = random.randint(2, 6)
    
    if num_bombs <= 3:
        num_diamonds = random.randint(6, 10)
        diamond_positions = random.sample(positions, num_diamonds)
    else:
        num_diamonds = random.randint(1, 3)
        diamond_positions = random.sample([0, 4, 10, 14, 20, 24], num_diamonds)
    
    matrix = ['⚫'] * 25
    
    for pos in diamond_positions:
        matrix[pos] = '💎'
    
    formatted_matrix = [matrix[i:i + 5] for i in range(0, 25, 5)]
    return num_bombs, formatted_matrix

async def send_mines_signal():
    while True:
        # Envia mensagem de "Buscando sinal 100%🔎…" e armazena a referência
        searching_message = await client.send_message(target_group_id, "Buscando sinal 100%🔎…")

        # Aguarda um tempo aleatório entre 1 a 3 minutos
        await asyncio.sleep(random.randint(60, 180))

        # Apaga a mensagem de "Buscando sinal 100%🔎…"
        await client.delete_messages(target_group_id, searching_message)

        # Gera o padrão de minas
        num_bombs, matrix = generate_mines_pattern()
        valido_ate = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")

        # Cria a mensagem do sinal
        matrix_str = '\n'.join([' '.join(row) for row in matrix])
        signal_message = (
            f"✅ ENTRADA CONFIRMADA ✅\n\n"
            f"JR Mines 💣\n\n"
            f"💣 Bombas: {num_bombs}\n"
            f"⏱ Valido até: {valido_ate}\n"
            f"📊 Chance de acerto: 100.00%\n"
            f"🔁 Nº de tentativas: 1\n\n"
            f"{matrix_str}"
        )

        # Envia a mensagem do sinal
        await client.send_message(target_group_id, signal_message)

        # Aguarda 1 minuto para que o sinal seja válido
        await asyncio.sleep(60)

        # Envia a mensagem de finalização do sinal
        final_message = (
            "🔴 SINAL FINALIZADO 🔴\n\n"
            "👇🏼 Se Cadastre na plataforma 👇🏼\n"
            "https://cl1ca.com/ClicouGanhou"
        )
        await client.send_message(target_group_id, final_message)

async def main():
    await send_mines_signal()

print("Bot está rodando...")
client.loop.run_until_complete(main())
