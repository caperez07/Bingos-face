import asyncio
from mqtt_test import send_mqtt


try:
    # Tenta obter o loop de eventos em execução
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # Se não houver um loop rodando, cria um novo
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Usa nest_asyncio para permitir eventos aninhados, caso seja necessário
    if loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
        # Executa a função MQTT no loop de evento já existente
        asyncio.ensure_future(send_mqtt())
    else:
        # Executa a função MQTT criando um novo loop de eventos
        loop.run_until_complete(send_mqtt())
except Exception as e:
    print(f"Erro no envio MQTT: {e}")
