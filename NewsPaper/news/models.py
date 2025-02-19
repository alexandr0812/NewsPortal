from django.db import models
from django.contrib.auth.models import User
from .resources import POST_TYPE_CHOICES, ARTICLE



class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author')
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Получаем все статьи автора
        articles = Post.objects.filter(author=self)

        # Суммируем рейтинг всех статей, умножая на 3
        article_rating = sum(article.rating for article in articles) * 3

        # Получаем все комментарии автора
        comments = Comment.objects.filter(users=self.user)

        # Суммируем рейтинг всех комментариев автора
        comment_rating = sum(comment.rating for comment in comments)

        # Получаем все комментарии к статьям автора
        article_comments = Comment.objects.filter(post__author=self)

        # Суммируем рейтинг всех комментариев к статьям
        article_comment_rating = sum(comment.rating for comment in article_comments)

        # Обновляем рейтинг автора
        self.rating = article_rating + comment_rating + article_comment_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=2, choices=POST_TYPE_CHOICES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory', related_name='posts')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()