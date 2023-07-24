import graphene
from graphene_django import DjangoObjectType
from .models import *
from asynch_notif.models import notification
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"
class SellerType(DjangoObjectType):
    class Meta:
        model=seller
        fields ="__all__"
class PostType(DjangoObjectType):
    class Meta:
        model=Post
        fields="__all__"
class OrderType(DjangoObjectType):
    class Meta:
        model=Order
        fields="__all__"
class ReviewType(DjangoObjectType):
    class Meta:
        model=reviews
        fields="__all__"
class NotificationType(DjangoObjectType):
    class Meta: 
        model = notification
        fields = ('id', 'sender', 'receiver', 'content')
class Query(graphene.ObjectType):
    seller_by_id = graphene.Field(graphene.List(SellerType), id=graphene.ID(required=True))
    post_by_id = graphene.Field(graphene.List(PostType), id=graphene.ID(required=True))
    all_posts = graphene.List(PostType)
    orders_by_seller_id = graphene.Field(graphene.List(OrderType), id=graphene.ID(required=True))
    reviews_by_post_id = graphene.Field(graphene.List(ReviewType), id = graphene.ID(required=True))
    Notification_by_reviever_id = graphene.Field(graphene.List(NotificationType), id = graphene.ID(required=True))
    def resolve_seller_by_id(root , info,id):
        return [seller.objects.get(id=id)]
    def resolve_posts_by_id(root , info, id):
        return Post.objects.get(id=id)
    def resolve_all_posts(root , info):
        return Post.objects.all()
    def resolve_orders_by_seller_id(root , info , id):
        return Order.objects.filter(seller__id=id)
    def resolve_reviews_by_post_id(root , info , id):
        return reviews.objects.filter(post__id=id)
    def resolve_Notification_by_reviever_id(root , info , id):
        return notification.objects.filter(reciever__id=id)
schema = graphene.Schema(query=Query)