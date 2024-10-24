from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class SavingsGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name='savings_groups')
    total_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    savings_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    payout_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field for payout amount
    members = models.ManyToManyField(User, related_name='savings_groups')

    def is_goal_met(self):
        return self.total_savings >= self.savings_goal

    def payout(self):
        if self.is_goal_met():
            # Logic to handle payouts
            # Reset total_savings or other logic can be implemented here
            payout_value = self.payout_amount
            self.total_savings -= payout_value
            self.save()
            return payout_value
        return None


    def __str__(self):
        return self.name

class Contribution(models.Model):
    group = models.ForeignKey(SavingsGroup, on_delete=models.CASCADE, related_name='contributions')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.username} contributed KSh {self.amount} to {self.group.name} on {self.date.strftime('%Y-%m-%d')}"
    
    
class FinancialLiteracyResource(models.Model):
        title = models.CharField(max_length=255)
        description = models.TextField()
        link = models.URLField()
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.title    
        
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)  # Store the correct answer
    options = models.JSONField()  # Store multiple options as a list

    def __str__(self):
        return self.question_text   
    
class Saving(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Savings"

class Transaction(models.Model):
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of {self.amount} on {self.created_at}"   

class Community(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities')
    members = models.ManyToManyField(User, related_name='communities', blank=True)

    def __str__(self):
        return self.name       
    

#model for the wallet
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def deposit(self, amount):
        """Add money to wallet"""
        self.balance += Decimal(amount)  # Convert amount to Decimal
        self.save()

    def withdraw(self, amount):
        """Withdraw money from wallet"""
        if self.balance >= Decimal(amount):  # Convert amount to Decimal
            self.balance -= Decimal(amount)  # Convert amount to Decimal
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.user.username}'s Wallet"
    
#news model
class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title