# REVISÃO DE EVERTON GABRIEL 

## Descrição: 
Essas correções tem o intuito de instruir o desenvolvedor que está começando a melhorar suas skills, aprender com `devs` mais experientes, além de direcionar para a cultura organizacional do time de tecnologia seguindo boas práticas de programação.

## Correções:

**Evitar problemas de N+1 na aplicação, criando soluções usando a ORM do Django e explorando os relacionamentos das tabelas ccom o QuerySet conforme passado já no documento em PDF anteriormente entregue e consultando a documentação oficial do Django.**

- Exemplo de código problemático

Buscando uma lista de livros e cada livros buscando o autor associado a ele.

```py

class ListBookView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    permission_classes = [AllowAny]
    
    queryset = Book.objects.all()
    
    serializer_class = BookSerializer
    
    OrderingFilter = ['title', 'publication_date', 'author__name','category', 'author', 'status']

```

Onde poderia ser

```py
class ListBookView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    permission_classes = [AllowAny]
    
    queryset = Book.objects.all().select_related('author')
    
    serializer_class = BookSerializer
    
    OrderingFilter = ['title', 'publication_date', 'author__name','category', 'author', 'status']
    
    def get_queryset(self):
        return super().get_queryset()
```

**Evitar deixar as funções fazer requisições sem um tratamento adequado, deixando as funções muito cruas e sem tratamento**

```py
class CreateBookView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Book.objects.all()
    
    serializer_class = BookSerializer
``` 

Como poderia ser 

```py
class CreateBookView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
```

Obs: o meu exemplo ainda está um pouco cru, pois para esse caso especifico poderiam ter várias validações, principalmente vindo do serializer onde voce pode serializar algum dado especifico para verificar se ele vem na requisição ou se é obrigatório, ou que seja essencial, ou até mesmo um serializer para atualizar e criar dados no banco, eu só dei um exemplo base para o desenvolvedor entender como melhorar o seu código.

**Faltou criar instruções claras de teste**

O teste é muito importante para validar se o endpoint está se comportando da forma que programamos, porem sem instruções claras de teste, dificulta o avaliador executar os testes ou até mesmo o desenvolvedor de executar esses testes.

**Configurações das variáveis de ambiente**

O desenvolvedor entregou o teste sem enviar as variáveis de ambiente, o que dificulta a validação de quem está responsável por avaliar o projeto, como é um teste, poderia deixar em string numa variável a key da api ou deixar algo mais profissional e realmente colocar em uma variável de ambiente, mas enviando tambem as configurações. 

**O README precisa ser corrigido**

Colocado em letras minúsculas, o "readme" é parte essencial do projeto e serve como um manual da aplicação, então não deve ser escrito de toda forma, principalmente como o github atua nos projetos, ele examina o projeto e publica como um manual de leitura se tiver com tudo maiúsculo. 

**Senha armazenada em texto puro**
  - `User` herda de `AbstractUser`, mas o model redefine `password = models.CharField(...)`.
  - `CreateUserSerializer` não sobrescreve `create` para chamar `user.set_password(...)`.
  - Isso faz com que a senha seja salva **sem hash**, o que é uma **falha gravíssima de segurança**.

**Autenticação duplicada/confusa**
  - Existe:
    - `AuthenticationService` com `check_password` manual e que funciona justamente porque ele simplesmente verifica se o texto puro da senha passada e da senha salva no sistema são iguais.
    - `SignInView` usando esse service.
    - Endpoints de JWT: `TokenObtainPairView` e `TokenRefreshView`.
    - `CustomTokenObtainPairSerializer`, mas não está plugado em nenhuma view customizada.
  - Resultado: o projeto mistura duas abordagens de login:
    - Uma manual `SignInView` + `AuthenticationService`).
    - Outra via SimpleJWT.
  - Para um júnior, é compreensível se perder aqui, principalmente com relação à escrita de senha, mas o ideal é **escolher uma abordagem e simplificar**.

**Fluxo de criação de usuário pouco intuitivo**
  - `UserCreate` é um `ListCreateAPIView` com `permission_classes = [IsAuthenticated]`.
  - Isso significa que, para criar usuário, **já precisa estar autenticado**, o que é estranho para fluxo de cadastro comum. Essa rota precisa estar `AllowAny`. O único modo de criação possível aqui seria através do Django Admin.
 
Só reforçando que estamos desenvolvendo uma API, então todo o contexto de desenvolvimento deve ter como base API Rest.