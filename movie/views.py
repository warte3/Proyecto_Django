from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64 


def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request,'home.html')
    #return render(request,'home.html',{'name':' Juan David'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html',{'searchTerm':searchTerm, 'movies':movies, 'name':' Juan David'})
def About(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')}
    return render(request,'about.html')


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})



def statistics_view(request):
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import io
    import base64
    
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {}
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = 'None'
        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    all_movies = Movie.objects.all()
    genre_counts = {}
    
    for movie in all_movies:
        if movie.genre:
            genres = movie.genre.split(',')
            first_genre = genres[0].strip() if genres else 'Unknown'
            
            if first_genre in genre_counts:
                genre_counts[first_genre] += 1
            else:
                genre_counts[first_genre] = 1
        else:
            if 'Unknown' in genre_counts:
                genre_counts['Unknown'] += 1
            else:
                genre_counts['Unknown'] = 1


    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))


    bar_positions1 = range(len(movie_counts_by_year))
    ax1.bar(bar_positions1, movie_counts_by_year.values(), width=0.5, align='center')
    ax1.set_title('Movies per year')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of movies')
    ax1.set_xticks(bar_positions1)
    ax1.set_xticklabels(movie_counts_by_year.keys(), rotation=90)


    bar_positions2 = range(len(genre_counts))
    ax2.bar(bar_positions2, genre_counts.values(), width=0.5, align='center', color='orange')
    ax2.set_title('Películas por Género (Primer Género)')
    ax2.set_xlabel('Género')
    ax2.set_ylabel('Número de Películas')
    ax2.set_xticks(bar_positions2)
    ax2.set_xticklabels(genre_counts.keys(), rotation=45, ha='right')


    plt.tight_layout()


    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'statistics.html', {'graphic': graphic})




