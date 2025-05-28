import React, { useEffect, useState } from 'react'

const initialForm = {
    placa: '',
    modelo: '',
    marca_id: 1,
    }

    const VehiculoForm = ({ onSubmit, vehiculoEdit, clearEdit }) => {
    const [form, setForm] = useState(initialForm)

    useEffect(() => {
        if (vehiculoEdit) {
        setForm(vehiculoEdit)
        }
    }, [vehiculoEdit])

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        if (vehiculoEdit) {
        onSubmit(vehiculoEdit.id, form)
        } else {
        onSubmit(form)
        }
        setForm(initialForm)
        clearEdit()
    }

    return (
        <form onSubmit={handleSubmit}>
        <input name="placa" value={form.placa} onChange={handleChange} placeholder="Placa" required />
        <input name="modelo" value={form.modelo} onChange={handleChange} placeholder="Modelo" required />
        <input type="number" name="marca_id" value={form.marca_id} onChange={handleChange} placeholder="Marca ID" />
        <button type="submit">{vehiculoEdit ? 'Actualizar' : 'Crear'}</button>
        </form>
    )
}

export default VehiculoForm
