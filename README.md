
## Configuração

Três arquivos básicos sustentam a parte de processamento do servidor

- `api.py` responsável por iniciar o nosso servidor que realizará a comununicação com o client-side
- `lsa_process.py` é responsável por executar os métodos referentes ao processamento do LSA
- `firebase.py` é responsável por estabelecer a conexação entre o Firebase Cloud Storage, no qual iremos buscar os arquivos que foram definidos pelo client-side

### Firebase

Para configurar o servidor para manipular as informações presentes no Firebase, precisamos alterar as credenciais vinculadas.
O arquivo `serviceAccountKey.json` é gerado no dashboard do Firebase Cloud Storage e deve ser inserido atualizado aqui. Ler [adicionar firebase a um servidor](https://firebase.google.com/docs/admin/setup#:~:text=To%20authenticate%20a%20service%20account,confirm%20by%20clicking%20Generate%20Key.).

A estrutura presente dentro do arquivo `firebase.py` deve ficar semelhante a esta, mas com as credenciais fornecidas.

```
firebaseConfig = {
  "apiKey": "",
  "authDomain": "",
  "projectId": "",
  "storageBucket": "",
  "databaseURL": "",
  "serviceAccount": "serviceAccountKey.json"
};
```

> **_📝NOTA:_**  Cloud storage foi usado aqui, mas pode ser substituído por qualquer outro a sua escolha. O importante é ter um local que armazene e sirva os documentos.

## Iniciar localmente

Necessário Python na versão `3.9.x`, outras versões não foram validadas.
Para configurar o ambiente pode ser necessário utilizar recursos como `pyenv` ou `conda`.

Veja [aqui](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) como criar um ambiente virtual em sua máquina definindo a versão do python.

Após isso instale todos as bibliotecas necessárias definidas no arquivo `requirements.txt`:

```
python3 install -r requirements.txt
```

Na sequência, com tudo instalado corretamente, execute:

```
python3 api.py
```
