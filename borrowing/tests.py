# borrowing/tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from django.contrib.auth import get_user_model
import uuid

# Importe seus modelos e serializers
from book.models import Book
from author.models import Author
from borrowing.models import Borrowing 

User = get_user_model()


class BorrowingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.borrowing_url = reverse('borrowing-create')
        self.today = timezone.now().date()
        self.return_date = self.today + timedelta(days=7)

        # 1. Criação de Usuários
        self.admin_user = User.objects.create_user(
            username='adminuser', 
            password='password123', 
            email='admin@test.com', 
            full_name='Admin User', 
            is_staff=True,
            is_superuser=True,
            status='active'
        )
        self.regular_user = User.objects.create_user(
            username='regularuser', 
            password='password123', 
            email='user@test.com', 
            full_name='Regular User', 
            status='active'
        )
        self.inactive_user = User.objects.create_user(
            username='inactiveuser', 
            password='password123', 
            email='inactive@test.com', 
            full_name='Inactive User', 
            status='inactive'
        )

        # 2. Geração de Tokens de Acesso
        self.admin_token = self._get_token(self.admin_user)
        self.user_token = self._get_token(self.regular_user)
        self.inactive_token = self._get_token(self.inactive_user)

        # 3. Criação de Dados de Livro
        self.author = Author.objects.create(
            name='Test Author', 
            birth_date='1980-01-01', 
            nationality='Fiction'
        )
        self.available_book = Book.objects.create(
            title='Available Book', 
            author=self.author, 
            category='FAN', 
            publisher='Pub', 
            publication_date='2020-01-01', 
            ISBN='1234567890123', 
            page_count=200, 
            last_edition='2020-01-01', 
            language='PT', 
            status='Available'
        )
        self.borrowed_book = Book.objects.create(
            title='Borrowed Book', 
            author=self.author, 
            category='FAN', 
            publisher='Pub', 
            publication_date='2020-01-01', 
            ISBN='1234567890124', 
            page_count=200, 
            last_edition='2020-01-01', 
            language='PT', 
            status='Borrowed'
        )

    # Função auxiliar para obter o token JWT (simulando o endpoint de login)
    def _get_token(self, user):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    # Função auxiliar para configurar o cliente com o token
    def _authenticate_client(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # =========================================================================
    # 2. TESTES DE REGRAS DE NEGÓCIO
    # =========================================================================

    def test_1_successful_borrowing_and_status_sync(self):
        """Testa o empréstimo bem-sucedido e se o status do livro muda para 'Borrowed'."""
        self._authenticate_client(self.user_token)
        
        data = {
            "user": self.regular_user.id, # Enviado, mas Serializer deve usar o logado (user_to_borrow_for)
            "book": self.available_book.id,
            "return_date": self.return_date.strftime('%Y-%m-%d')
        }
        
        response = self.client.post(self.borrowing_url, data, format='json')
        
        # O teste deve passar com o status 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se o status do livro foi atualizado no banco de dados
        self.available_book.refresh_from_db()
        self.assertEqual(self.available_book.status, 'Borrowed')
        
        # Verifica se o empréstimo foi criado para o usuário correto
        self.assertEqual(Borrowing.objects.get().user, self.regular_user)


    def test_2_cannot_borrow_unavailable_book(self):
        """Testa se o Serializer impede o empréstimo de um livro com status 'Borrowed'."""
        self._authenticate_client(self.user_token)
        
        data = {
            "user": self.regular_user.id,
            "book": self.borrowed_book.id,
            "return_date": self.return_date.strftime('%Y-%m-%d')
        }
        
        response = self.client.post(self.borrowing_url, data, format='json')
        
        # O teste deve falhar com o status 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('O livro', response.data['book'][0])
        self.assertIn('Borrowed', response.data['book'][0])

        # Verifica se o status do livro NÃO mudou
        self.borrowed_book.refresh_from_db()
        self.assertEqual(self.borrowed_book.status, 'Borrowed')


    def test_3_maximum_borrowing_limit(self):
        """Testa se o Serializer impede o empréstimo se o limite de 5 livros for atingido."""
        self._authenticate_client(self.user_token)
        
        # Cria 5 empréstimos ativos para o usuário regular
        for i in range(5):
             book = Book.objects.create(
                title=f'Livro {i+1}', author=self.author, category='FIC', publisher='Pub', 
                publication_date='2020-01-01', ISBN=f'999999999999{i}', page_count=100, 
                last_edition='2020-01-01', language='PT', status='Available'
            )
             Borrowing.objects.create(user=self.regular_user, book=book, status='OUT')

        # Tenta criar o 6º empréstimo
        data = {
            "user": self.regular_user.id,
            "book": self.available_book.id,
            "return_date": self.return_date.strftime('%Y-%m-%d')
        }
        
        response = self.client.post(self.borrowing_url, data, format='json')
        
        # O teste deve falhar com 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('excedeu o limite de cinco', response.data['user'][0])


    def test_4_admin_can_borrow_for_another_user(self):
        """Testa se o Admin consegue criar um empréstimo para um usuário diferente."""
        self._authenticate_client(self.admin_token)
        
        data = {
            "user": self.regular_user.id, # Admin logado, mas emprestando para o regular_user
            "book": self.available_book.id,
            "return_date": self.return_date.strftime('%Y-%m-%d')
        }
        
        response = self.client.post(self.borrowing_url, data, format='json')
        
        # Deve ter sucesso (201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verifica se o empréstimo foi criado para o usuário CORRETO (regular_user)
        self.assertEqual(Borrowing.objects.get().user, self.regular_user)
        
    
    def test_5_common_user_cannot_borrow_for_another_user(self):
        """Testa se o usuário comum é impedido de criar empréstimos para outros."""
        self._authenticate_client(self.user_token) # Usuário regular logado
        
        data = {
            "user": self.admin_user.id, # Tentando emprestar para o Admin
            "book": self.available_book.id,
            "return_date": self.return_date.strftime('%Y-%m-%d')
        }
        
        response = self.client.post(self.borrowing_url, data, format='json')
        
        # Deve falhar com 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Usuários comuns só podem criar empréstimos para si mesmos', response.data['user'][0])
        

    def test_6_cannot_borrow_if_user_is_inactive(self):
        """Testa se usuários inativos são impedidos de realizar empréstimos."""
        self._authenticate_client(self.inactive_token)
        
        data = {
            "user": self.inactive_user.id, 
            "book": self.available_book.id,
            "return_date": self.return_date.strftime('%Y-%m-%d')
        }
        
        response = self.client.post(self.borrowing_url, data, format='json')
        
        # Deve falhar com 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('está inativo e não pode realizar empréstimos', response.data['user'][0])
        
    
    def test_7_cannot_borrow_with_invalid_return_date(self):
        """Testa se o empréstimo é bloqueado com uma data de devolução inválida (passado)."""
        self._authenticate_client(self.user_token)
        
        data = {
            "user": self.regular_user.id, 
            "book": self.available_book.id,
            "return_date": (self.today - timedelta(days=1)).strftime('%Y-%m-%d') # Data de ontem
        }
        
        response = self.client.post(self.borrowing_url, data, format='json')
        
        # Deve falhar com 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('A data de devolução deve ser posterior à data de empréstimo', response.data['return_date'][0])
        

