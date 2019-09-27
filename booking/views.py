from django.shortcuts import render, redirect


# Create your views here.

def booking_index(request):
    return render(request,'index.html',)

# def query_member(request):
#     return render
#
#
# def insert_member(request):
#     return redirect
