
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError
from django.utils import timezone

from .models import Cliente, Cita


# =====================================
# PÁGINA PRINCIPAL
# =====================================

@login_required
def inicio(request):

    total_clientes = Cliente.objects.count()
    total_citas = Cita.objects.count()

    citas_virtuales = Cita.objects.filter(
        tipo_reunion="Virtual"
    ).count()

    citas_presenciales = Cita.objects.filter(
        tipo_reunion="Presencial"
    ).count()

    proximas_citas = (
        Cita.objects.select_related("cliente")
        .filter(fecha_hora__gte=timezone.now())
        .order_by("fecha_hora")[:5]
    )

    return render(request, "control/inicio.html", {
        "total_clientes": total_clientes,
        "total_citas": total_citas,
        "citas_virtuales": citas_virtuales,
        "citas_presenciales": citas_presenciales,
        "proximas_citas": proximas_citas,
    })


# =====================================
# CLIENTES: LISTAR Y BUSCAR
# =====================================

@login_required
def clientes(request):

    lista = Cliente.objects.all().order_by("-id_cliente")

    buscar = request.GET.get("buscar", "").strip()

    if buscar:
        lista = lista.filter(
            Q(nombre__icontains=buscar) |
            Q(apellido__icontains=buscar) |
            Q(dni__icontains=buscar)
        )

    # CARGAR UN CLIENTE PARA EDITAR
    editar_id = request.GET.get("editar", "").strip()

    editar = None

    if editar_id:
        editar = get_object_or_404(
            Cliente,
            id_cliente=editar_id
        )

    return render(request, "control/clientes.html", {
        "clientes": lista,
        "buscar": buscar,
        "editar": editar
    })


# =====================================
# CLIENTES: GUARDAR O ACTUALIZAR
# =====================================

@login_required
@require_POST
def guardar_cliente(request):

    nombre = request.POST.get("nombre", "").strip()
    apellido = request.POST.get("apellido", "").strip()
    correo = request.POST.get("correo", "").strip()
    telefono = request.POST.get("telefono", "").strip()
    dni = request.POST.get("dni", "").strip()
    edad = request.POST.get("edad", "").strip()
    peso = request.POST.get("peso", "").strip()

    id_cliente = request.POST.get("id_cliente", "").strip()

    # VALIDAR CAMPOS OBLIGATORIOS
    if not all([
        nombre, apellido, correo,
        telefono, dni, edad, peso
    ]):
        messages.error(request, "Completa todos los campos.")
        return redirect("clientes")

    # VALIDAR DNI
    if len(dni) != 8 or not dni.isdigit():
        messages.error(request, "El DNI debe tener 8 dígitos.")
        return redirect("clientes")

    # VALIDAR EDAD Y PESO
    try:
        edad = int(edad)
        peso = float(peso)

        if edad < 0 or edad > 150 or peso <= 0:
            raise ValueError

    except ValueError:
        messages.error(request, "Edad o peso no válidos.")
        return redirect("clientes")

    try:
        if id_cliente:
            # ACTUALIZAR
            cliente = get_object_or_404(
                Cliente,
                id_cliente=id_cliente
            )

            cliente.nombre = nombre
            cliente.apellido = apellido
            cliente.correo = correo
            cliente.telefono = telefono
            cliente.dni = dni
            cliente.edad = edad
            cliente.peso = peso

            cliente.save()

            messages.success(
                request,
                "Cliente actualizado correctamente."
            )

        else:
            # GUARDAR NUEVO
            Cliente.objects.create(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                telefono=telefono,
                dni=dni,
                edad=edad,
                peso=peso
            )

            messages.success(
                request,
                "Cliente guardado correctamente."
            )

    except IntegrityError:
        messages.error(
            request,
            "El DNI ya está registrado."
        )

    return redirect("clientes")


# =====================================
# CLIENTES: ELIMINAR
# =====================================

@login_required
@require_POST
def eliminar_cliente(request, id):

    cliente = get_object_or_404(
        Cliente,
        id_cliente=id
    )

    # NO ELIMINAR SI TIENE CITAS
    if cliente.citas.exists():
        messages.error(
            request,
            "No puedes eliminar un cliente que tiene citas."
        )
    else:
        cliente.delete()
        messages.success(
            request,
            "Cliente eliminado correctamente."
        )

    return redirect("clientes")


# =====================================
# CITAS: LISTAR Y BUSCAR
# =====================================

@login_required
def citas(request):

    lista = Cita.objects.select_related(
        "cliente"
    ).order_by("fecha_hora")

    buscar = request.GET.get("buscar", "").strip()

    if buscar:
        lista = lista.filter(
            Q(cliente__nombre__icontains=buscar) |
            Q(cliente__apellido__icontains=buscar) |
            Q(motivo__icontains=buscar)
        )

    # CARGAR CITA PARA EDITAR
    editar_id = request.GET.get("editar", "").strip()

    editar = None

    if editar_id:
        editar = get_object_or_404(
            Cita,
            id_cita=editar_id
        )

    lista_clientes = Cliente.objects.all().order_by("nombre")

    return render(request, "control/citas.html", {
        "citas": lista,
        "clientes": lista_clientes,
        "buscar": buscar,
        "editar": editar
    })


# =====================================
# CITAS: GUARDAR O ACTUALIZAR
# =====================================

@login_required
@require_POST
def guardar_cita(request):

    from datetime import datetime
    from django.utils import timezone

    id_cita = request.POST.get("id_cita", "").strip()
    id_cliente = request.POST.get("id_cliente", "").strip()
    fecha_hora = request.POST.get("fecha_hora", "").strip()
    motivo = request.POST.get("motivo", "").strip()
    tipo_reunion = request.POST.get("tipo_reunion", "").strip()
    direccion = request.POST.get("direccion", "").strip()
    referencia = request.POST.get("referencia", "").strip()
    enlace_virtual = request.POST.get("enlace_virtual", "").strip()

    # VALIDAR CAMPOS
    if not id_cliente or not fecha_hora or not motivo:
        messages.error(
            request,
            "Completa cliente, fecha y motivo."
        )
        return redirect("citas")

    if tipo_reunion not in ["Virtual", "Presencial"]:
        messages.error(request, "Selecciona el tipo de reunión.")
        return redirect("citas")

    # CONVERTIR LA FECHA RECIBIDA
    try:
        fecha = datetime.strptime(
            fecha_hora,
            "%Y-%m-%dT%H:%M"
        )

        fecha = timezone.make_aware(
            fecha,
            timezone.get_current_timezone()
        )

    except (ValueError, OverflowError):
        messages.error(request, "Fecha y hora no válidas.")
        return redirect("citas")

    cliente = get_object_or_404(
        Cliente,
        id_cliente=id_cliente
    )

    # DEJAR VACÍOS LOS CAMPOS QUE NO CORRESPONDEN
    if tipo_reunion == "Virtual":
        direccion = ""
        referencia = ""
    else:
        enlace_virtual = ""

    if id_cita:
        # ACTUALIZAR CITA
        cita = get_object_or_404(
            Cita,
            id_cita=id_cita
        )

        cita.cliente = cliente
        cita.fecha_hora = fecha
        cita.motivo = motivo
        cita.tipo_reunion = tipo_reunion
        cita.direccion = direccion
        cita.referencia = referencia
        cita.enlace_virtual = enlace_virtual

        cita.save()

        messages.success(request, "Cita actualizada.")

    else:
        # GUARDAR CITA NUEVA
        Cita.objects.create(
            cliente=cliente,
            fecha_hora=fecha,
            motivo=motivo,
            tipo_reunion=tipo_reunion,
            direccion=direccion,
            referencia=referencia,
            enlace_virtual=enlace_virtual
        )

        messages.success(request, "Cita guardada.")

    return redirect("citas")


# =====================================
# CITAS: ELIMINAR
# =====================================

@login_required
@require_POST
def eliminar_cita(request, id):

    cita = get_object_or_404(
        Cita,
        id_cita=id
    )

    cita.delete()

    messages.success(
        request,
        "Cita eliminada correctamente."
    )

    return redirect("citas")
