from django.shortcuts import render
from .helpers import main, get_df


def index(request):
    context = {}
    return render(request, "search_engine/index.html", context)


def results(request):
    link_results = []
    query = request.GET.get('query')
    if request.method == "POST":
        if request.POST.get('search-input'):
            query = request.POST['search-input']
            results_ = main(query)
            df = get_df()
            if results_:
                for res in results_:
                    link = [res[0], df.at[res[0], 'member_name'] + "/" + df.at[res[0], 'political_party'] + "/" +
                            df.at[res[0], 'sitting_date']]
                    link_results.append(link)

    context = {
        "link_results": link_results,
        "query": query,
    }
    return render(request, "search_engine/results.html", context)


def speech(request):
    doc = int(request.GET.get('doc'))
    df = get_df()

    member_name = df.at[doc, 'member_name']
    political_party = df.at[doc, 'political_party']
    speech_ = df.at[doc, 'speech']
    date = df.at[doc, 'sitting_date']
    role = df.at[doc, 'roles']
    role = role[1: -1]
    context = {
        'doc': doc,
        'member_name': member_name,
        'political_party': political_party,
        'speech': speech_,
        'date': date,
        'role': role
    }
    return render(request, "search_engine/speech.html", context)
