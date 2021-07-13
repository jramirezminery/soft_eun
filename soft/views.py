from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta
from dateutil import tz, parser
from soft.auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token, get_token
from soft.graph_helper import *
from soft.sql_helper import get_all_levels, get_all_titles, get_all_titles_with_levels

# <HomeViewSnippet>
def home(request):
  context = initialize_context(request)

  return render(request, 'views/home.html', context)
# </HomeViewSnippet>

# <InitializeContextSnippet>
def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context
# </InitializeContextSnippet>

# <SignInViewSnippet>
def sign_in(request):
  # Get the sign-in flow
  flow = get_sign_in_flow()
  # Save the expected flow so we can use it in the callback
  try:
    request.session['auth_flow'] = flow
  except Exception as e:
    print(e)
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(flow['auth_uri'])
# </SignInViewSnippet>

# <SignOutViewSnippet>
def sign_out(request):
  # Clear out the user and token
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))
# </SignOutViewSnippet>

# <CallbackViewSnippet>
def callback(request):
  # Make the token request
  result = get_token_from_code(request)

  #Get the user's profile
  user = get_user(result['access_token'])

  # Store user
  store_user(request, user)
  return HttpResponseRedirect(reverse('home'))
# </CallbackViewSnippet>

# <DrivesViewSnippet>
def drives(request):
  context = initialize_context(request)
  user = context['user']

  token = get_token(request)

  # drivesId = get_drives_ids(token, get_my_organization_drives(token, user['timeZone'])["id"], user['timeZone'])
  drivesId = get_drives_ids(token, 'solucionesroots.sharepoint.com,1dd1c895-fe68-457c-a4ba-8c20fc92b8c0,403d5c33-99ca-44a4-a2cb-7a4e1ebdd14f', user['timeZone'])

  context['drives'] = drivesId['value']

  return render(request, 'views/drives.html', context)
# </DrivesViewSnippet>

# <DrivesListViewSnippet>
def list_drives(request, id):
  context = initialize_context(request)
  user = context['user']

  token = get_token(request)

  drivesId = get_list_drive(token, id , user['timeZone'])

  context['driveslist'] = drivesId['value']

  return render(request, 'views/drives_list.html', context)
# </DrivesListViewSnippet>

# <DrivesFolderListViewSnippet>
def list_drives_with_folder(request, id):
  context = initialize_context(request)
  user = context['user']

  token = get_token(request)

  drivesId = get_list_drive_folder(token, 'b!lcjRHWj-fEWkuowg_JK4wDNcPUDKmaREost6Th690U-yZsnQo2CEQr8gFH8_fVC-', id , user['timeZone'])

  context['driveslistfolder'] = drivesId['value']

  return render(request, 'views/drives_folder_list.html', context)
# </DrivesFolderListViewSnippet>

# <CalendarViewSnippet>
def calendar(request):
  context = initialize_context(request)
  user = context['user']

  # Load the user's time zone
  # Microsoft Graph can return the user's time zone as either
  # a Windows time zone name or an IANA time zone identifier
  # Python datetime requires IANA, so convert Windows to IANA
  time_zone = get_iana_from_windows(user['timeZone'])
  tz_info = tz.gettz(time_zone)
  

  # Get midnight today in user's time zone
  today = datetime.now(tz_info).replace(
    hour=0,
    minute=0,
    second=0,
    microsecond=0)

  # Based on today, get the start of the week (Sunday)
  if (today.weekday() != 6):
    start = today - timedelta(days=today.isoweekday())
  else:
    start = today

  end = start + timedelta(days=7)

  token = get_token(request)

  events = get_calendar_events(
    token,
    start.isoformat(timespec='seconds'),
    end.isoformat(timespec='seconds'),
    user['timeZone'])

  if events:
    # Convert the ISO 8601 date times to a datetime object
    # This allows the Django template to format the value nicely
    for event in events['value']:
      event['start']['dateTime'] = parser.parse(event['start']['dateTime'])
      event['end']['dateTime'] = parser.parse(event['end']['dateTime'])

    context['events'] = events['value']

  return render(request, 'views/calendar.html', context)
# </CalendarViewSnippet>

# <NewEventViewSnippet>
def newevent(request):
  context = initialize_context(request)
  user = context['user']

  if request.method == 'POST':
    # Validate the form values
    # Required values
    if (not request.POST['ev-subject']) or \
       (not request.POST['ev-start']) or \
       (not request.POST['ev-end']):
      context['errors'] = [
        { 'message': 'Invalid values', 'debug': 'The subject, start, and end fields are required.'}
      ]
      return render(request, 'views/newevent.html', context)

    attendees = None
    if request.POST['ev-attendees']:
      attendees = request.POST['ev-attendees'].split(';')
    body = request.POST['ev-body']

    # Create the event
    token = get_token(request)

    create_event(
      token,
      request.POST['ev-subject'],
      request.POST['ev-start'],
      request.POST['ev-end'],
      attendees,
      request.POST['ev-body'],
      user['timeZone'])

    # Redirect back to calendar view
    return HttpResponseRedirect(reverse('calendar'))
  else:
    # Render the form
    return render(request, 'views/newevent.html', context)
  print('hello')
# </NewEventViewSnippet>

# <LevelListViewSnippet>
def level(request):
  context = initialize_context(request)

  for p in get_all_titles_with_levels(str(2)):
    print(p)

  return render(request, 'views/login/level.html', context)
# </LevelListViewSnippet>