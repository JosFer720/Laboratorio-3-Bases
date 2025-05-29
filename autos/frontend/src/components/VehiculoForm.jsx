import React, { useEffect, useState } from 'react';

const initialForm = {
    placa: '',
    modelo: '',
    marca_id: 1,
    };

const VehiculoForm = ({ onSubmit, vehiculoEdit, clearEdit }) => {
    const [form, setForm] = useState(initialForm);

    useEffect(() => {
        if (vehiculoEdit) setForm(vehiculoEdit);
    }, [vehiculoEdit]);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (vehiculoEdit) {
        onSubmit(vehiculoEdit.id, form);
        } else {
        onSubmit(form);
        }
        setForm(initialForm);
        clearEdit();
    };

    return (
        <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-xl p-6 max-w-md mx-auto mt-6 space-y-4">
        <h2 className="text-xl font-semibold">{vehiculoEdit ? 'Editar Vehículo' : 'Registrar Vehículo'}</h2>

        <input
            name="placa"
            value={form.placa}
            onChange={handleChange}
            placeholder="Placa"
            required
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <input
            name="modelo"
            value={form.modelo}
            onChange={handleChange}
            placeholder="Modelo"
            required
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <input
            type="number"
            name="marca_id"
            value={form.marca_id}
            onChange={handleChange}
            placeholder="Marca ID"
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <div className="flex justify-end gap-2">
            <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
            >
            {vehiculoEdit ? 'Actualizar' : 'Crear'}
            </button>
            {vehiculoEdit && (
            <button
                type="button"
                onClick={clearEdit}
                className="bg-gray-300 hover:bg-gray-400 text-black px-4 py-2 rounded-md"
            >
                Cancelar
            </button>
            )}
        </div>
        </form>
    );
};

export default VehiculoForm;
