import graphene
from graphene_django import DjangoObjectType
from .models import *
class SellerType(DjangoObjectType):
    class Meta:
        model=seller
        fields ="__all__"
class Query(graphene.ObjectType):
    all_sellers = graphene.List(SellerType)
    seller_by_id = graphene.Field(graphene.List(SellerType), id=graphene.ID(required=True))
    def resolve_seller_by_id(root , info,id):
        return [seller.objects.get(id=id)]
    def resolve_all_sellers(root , info):
        return seller.objects.all()
schema = graphene.Schema(query=Query)