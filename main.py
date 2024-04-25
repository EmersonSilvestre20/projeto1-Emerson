import mysql.connector
import psycopg2

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )

def user_login(cursor, email, senha):
    query = "SELECT * FROM usuarios WHERE email = %s AND senha = %s"
    cursor.execute(query, (email, senha))
    return cursor.fetchone()

def user_registration(cursor, nome_completo, nome_usuario, email, senha):
    query = "INSERT INTO usuarios (nome_completo, nome_usuario, email, senha) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nome_completo, nome_usuario, email, senha))

def edit_user_profile(cursor, user_id, new_full_name, new_username):
    try:
        # Verificar se o novo nome de usuário é único
        check_query = "SELECT id FROM usuarios WHERE nome_usuario = %s AND id != %s"
        cursor.execute(check_query, (new_username, user_id))
        existing_user = cursor.fetchone()

        if existing_user:
            print("Erro: O novo nome de usuário já está em uso. Escolha outro.")
            return

        # Atualizar perfil no banco de dados
        update_query = "UPDATE usuarios SET nome_completo = %s, nome_usuario = %s WHERE id = %s"
        cursor.execute(update_query, (new_full_name, new_username, user_id))
        db_connection.commit()

        print("Perfil atualizado com sucesso!")

    except Exception as e:
        print(f"Erro ao atualizar perfil: {e}")

def privacy_settings_menu():
    print("=" * 100)
    print("\t\t\t\t\tConfigurações de Privacidade")
    print("=" * 100)
    print("1. Definir quem pode ver seus Pins")
    print("2. Definir quem pode ver seus Boards")
    print("3. Voltar")

def privacy_settings(user_id, cursor):
    while True:
        privacy_settings_menu()
        choice = int(input("Escolha uma opção: "))

        if choice == 1:
            visibility = input("Quem pode ver seus Pins (público/privado/amigos): ")
            update_query = "UPDATE usuarios SET pins_visibility = %s WHERE id = %s"
            cursor.execute(update_query, (visibility, user_id))
            db_connection.commit()
            print("Configuração de privacidade para Pins atualizada com sucesso!")

        elif choice == 2:
            visibility = input("Quem pode ver seus Boards (público/privado/amigos): ")
            update_query = "UPDATE usuarios SET boards_visibility = %s WHERE id = %s"
            cursor.execute(update_query, (visibility, user_id))
            db_connection.commit()
            print("Configuração de privacidade para Boards atualizada com sucesso!")

        elif choice == 3:
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

def view_pins_menu():
    print("=" * 100)
    print("\t\t\t\t\tVisualizar Pins")
    print("=" * 100)
    print("1. Listar Meus Pins")
    print("2. Listar Pins de um Board")
    print("3. Criar novo Pin")
    print("4. Voltar")

def create_pin(cursor, user_id, pin_type, content, board_id):
    try:
        # Insere um novo Pin na base de dados
        query = "INSERT INTO pins (user_id, pin_type, content, board_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, pin_type, content, board_id))
        db_connection.commit()
        print("Pin criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar Pin: {e}")

def list_user_pins(cursor, user_id):
    try:
        # Lista os Pins do usuário
        query = "SELECT id, pin_type, content, board_id FROM pins WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        pins = cursor.fetchall()

        if not pins:
            print("Nenhum Pin encontrado para este usuário.")
        else:
            print("=" * 100)
            print("\t\t\t\t\tLista de Pins")
            print("=" * 100)
            for pin in pins:
                pin_id, pin_type, content, board_id = pin
                print(f"ID: {pin_id}, Tipo: {pin_type}, Conteúdo: {content}, Board ID: {board_id}")
    except Exception as e:
        print(f"Erro ao listar Pins: {e}")

def list_board_pins(cursor, board_id):
    try:
        # Lista os Pins de um Board específico
        query = "SELECT id, pin_type, content FROM pins WHERE board_id = %s"
        cursor.execute(query, (board_id,))
        board_pins = cursor.fetchall()

        if not board_pins:
            print("Nenhum Pin encontrado para este Board.")
        else:
            print("=" * 100)
            print(f"\t\t\t\t\tLista de Pins do Board {board_id}")
            print("=" * 100)
            for pin in board_pins:
                pin_id, pin_type, content = pin
                print(f"ID: {pin_id}, Tipo: {pin_type}, Conteúdo: {content}")
    except Exception as e:
        print(f"Erro ao listar Pins do Board: {e}")

def view_pins(user_id, cursor):
    while True:
        view_pins_menu()
        choice = int(input("Escolha uma opção: "))

        if choice == 1:
            list_user_pins(cursor, user_id)
        elif choice == 2:
            board_id = int(input("Digite o ID do Board: "))
            list_board_pins(cursor, board_id)
        elif choice == 3:
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

def view_user_profile(user_data, cursor):
    user_id = user_data[0]
    nome_usuario = user_data[2]

    print(f"Visualizando perfil de {nome_usuario}.")

    while True:
        print("=" * 100)
        print("\t\t\t\t\tOpções do Perfil")
        print("=" * 100)
        print("1. Visualizar Pins")
        print("2. Visualizar Boards")
        print("3. Configurações de Privacidade")
        print("4. Voltar")

        user_choice = int(input("Escolha uma opção: "))

        if user_choice == 1:
            view_pins(user_id, cursor)
        elif user_choice == 2:
            # Lógica para visualizar Boards
            print("Visualizando Boards...")
        elif user_choice == 3:
            privacy_settings(user_id, cursor)
        elif user_choice == 4:
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# Código principal
print("=" * 100)
print("\t\t\t\t\t\tBem-vindo ao login")
print("=" * 100)

print("-" * 100)
print("\t\t\t\t\tMenu Pinterest \n1-Login\n2-Cadastro")
choice = int(input("=>"))
print("-" * 100)

db_connection = connect_to_database()
cursor = db_connection.cursor()

if choice == 1:
    print("-" * 100)
    print("\t\t\t\t\tLogin Pinterest")
    print("-" * 100)

    email = input("E-mail: ")
    senha = input("Senha: ")

    user_data = user_login(cursor, email, senha)

    if user_data:
        nome_usuario = user_data[2]  # Assumindo que o nome do usuário está na terceira coluna
        print(f"Login bem-sucedido para {nome_usuario}!")

        # Adicione a área do usuário com um menu
        while True:
            view_user_profile(user_data, cursor)
            user_choice = int(input("Escolha uma opção na Área do Usuário: "))
            if user_choice == 1:
                view_pins(user_data[0], cursor)
            elif user_choice == 2:
                # Lógica para visualizar Boards
                print("Visualizando Boards...")
            elif user_area_options(user_choice, nome_usuario):
                break  # Sai do loop se o usuário escolher sair

    else:
        print("Login falhou. Por favor, verifique suas credenciais.")

elif choice == 2:
    print("-" * 100)
    print("\t\t\t\t\tCadastre-se no Pinterest")
    print("-" * 100)

    nome_completo = input("Nome Completo: ")
    nome_usuario = input("Nome de Usuário: ")
    email = input("E-mail: ")
    senha = input("Senha: ")

    user_registration(cursor, nome_completo, nome_usuario, email, senha)
    db_connection.commit()
    print("Cadastro realizado com sucesso!")

cursor.close()
db_connection.close()
