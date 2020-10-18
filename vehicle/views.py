"""Module contains view functions for the vechile app"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.urls import reverse

from helper.utility import Utility
from .models import Vehicle, VehicleType, FUEL_TYPE_CHOICES
from .forms import VehicleForm

@login_required
def vehicle_listing(request):
    """Function to render vechile listing page.

    Args:
        request: HttpRequest object.

    Returns:
        JsonResponse object.
    """
    return render(request, 'home.html', {
        'vehicle_types': VehicleType.objects.all()
    })

@login_required
@require_POST
def vehicle_listing_data(request):
    """Function to list all the vehicle details.

    This method is called via ajax from the home page to provide data to the datatables plugin.

    Args:
        request: HttpRequest object.

    Returns:
        JsonResponse object.
    """
    response = {
        'draw': 1,
        'recordsTotal': 0,
        'recordsFiltered': 0,
        'data': []
    }

    # Get the logger instance
    logger = Utility().get_logger()

    try:
        try:
            vechicle_type =  int(request.GET.get('vechicleType', 0))
        except ValueError:
            vechicle_type = 0

        if vechicle_type:
            # Converts tuple into a dict.
            fuel_types = dict(FUEL_TYPE_CHOICES)

            columns = {
                0: 'name',
                1: 'model',
                2: 'price',
                3: 'fuel_type'
            }

            # Draw counter. Sent by the databale to identify ajax request order.
            # We have return this in the response.
            draw = int(request.POST.get('draw', 0))

            # Pagination data. '0' will be first page.
            start = int(request.POST.get('start', 0))

            # Number of records to display. This is the limit value.
            length = int(request.POST.get('length', 0))

            # Value entered in the search input
            search_string = request.POST.get('search[value]')

            # Column index of the column on which sorting is to be done.
            order_column = int(request.POST.get('order[0][column]', 0))

            # Order type 'asc' or 'desc'
            order_type = request.POST.get('order[0][dir]', 'asc')
            order_type = False if order_type == 'asc' else True

            # Gets the all vehicle data of the user by vechile type
            vehicles = Vehicle.objects.filter(user=request.user.id, vehicle_type=vechicle_type)

            # Sorting data
            if order_type: # Desc
                vehicles = vehicles.order_by('-' + columns.get(order_column))
            else: # Asc
                vehicles = vehicles.order_by(columns.get(order_column))

            # Gets Total records, before filtering
            records_total = vehicles.count()

            # Applying search filtering
            if search_string:
                vehicles = vehicles.filter(
                    Q(name__icontains=search_string) | Q(model__icontains=search_string)
                )
                # Total records, after filtering
                records_filtered = vehicles.count()
            else:
                records_filtered = records_total

            # Applying pagination
            vehicles = vehicles[start: (start + length)]

            edit_button = '<a href="[[url]]" class="btn btn-info btn-sm">Edit</a>'
            delete_button = '<a href="[[url]]" class="btn btn-danger btn-sm">Delete</a>'

            list_data = []
            for vehicle in vehicles:
                list_data.append([
                    vehicle.name,
                    vehicle.model,
                    vehicle.price,
                    fuel_types.get(vehicle.fuel_type, '-'),
                    '&nbsp;'.join([
                        edit_button.replace('[[url]]', reverse('vehicle-edit', args=[vehicle.vehicle_id])),
                        delete_button.replace('[[url]]', reverse('vehicle-delete', args=[vehicle.vehicle_id])),
                    ])
                ])

            # Returning response
            response['draw'] = draw
            response['recordsTotal'] = records_total
            response['recordsFiltered'] = records_filtered
            response['data'] = list_data
    except Exception as error:
        response['recordsTotal'] = 0
        response['recordsFiltered'] = 0
        response['data'] = []
        logger.error(
            'Error in the vehicle_listing_data view function'
            f'Error: {str(error)}, Error traceback: {Utility.get_exception()}'
        )
    return JsonResponse(response)

@login_required
def create_vechicle(request):
    """Function to render vechile create form

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object contiaing html.
    """
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('home')
    else:
        form = VehicleForm(initial={'user': request.user})
    return render(request, 'vehicle_form.html', {
        'form': form,
        'action_type': 'create'
    })

@login_required
def edit_vechicle(request, vehicle_id):
    """Function to render vechile edit form

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object contiaing html.
    """
    vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
    if vehicle:
        if request.method == 'POST':
            form = VehicleForm(instance=vehicle, data=request.POST)
            if form.is_valid():
                form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect('home')
        else:
            form = VehicleForm(initial={
                'name': vehicle.name,
                'model': vehicle.model,
                'price': vehicle.price,
                'fuel_type': vehicle.fuel_type,
                'vehicle_type': vehicle.vehicle_type.id,
                'user': request.user
            })

        return render(request, 'vehicle_form.html', {
            'form': form,
            'action_type': 'edit'
        })
    else:
        raise Exception('Vehicle Not Found')

@login_required
def delete_vechicle(request, vehicle_id):
    """Function to delete vechile.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponseRedirect  object.
    """
    vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
    if vehicle:
        vehicle.delete()
    else:
        raise Exception('Vehicle Not Found')
    return redirect('home')
