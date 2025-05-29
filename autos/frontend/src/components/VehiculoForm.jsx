import React, { useEffect, useState } from "react";

const initialForm = {
  id: null, // para edición, null si es nuevo
  marca_id: "",
  modelo: "",
  anio: "",
  tipo: "",
  descripcion: "",
  precio: "",
  vendedor_id: "",
  disponible: true,
  categorias: [], // lista de IDs numéricos
};

const VehiculoForm = ({ onSubmit, vehiculoEdit, clearEdit }) => {
  const [form, setForm] = useState(initialForm);

  useEffect(() => {
    if (vehiculoEdit) {
      // Al cargar un vehículo para editar, asegurarse que categorías sean array de números
      setForm({
        ...vehiculoEdit,
        categorias:
          Array.isArray(vehiculoEdit.categorias)
            ? vehiculoEdit.categorias.map((cat) =>
                typeof cat === "object" ? cat.id : cat
              )
            : [],
      });
    } else {
      setForm(initialForm);
    }
  }, [vehiculoEdit]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (name === "categorias") {
      // Convertir input string "1,2,3" a array de números
      const cats = value
        .split(",")
        .map((id) => Number(id.trim()))
        .filter((id) => !isNaN(id));
      setForm((prev) => ({ ...prev, categorias: cats }));
    } else if (type === "checkbox") {
      setForm((prev) => ({ ...prev, [name]: checked }));
    } else if (type === "number") {
      setForm((prev) => ({ ...prev, [name]: value === "" ? "" : Number(value) }));
    } else {
      setForm((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validar campos obligatorios
    if (
      !form.marca_id ||
      !form.modelo ||
      !form.anio ||
      !form.precio ||
      !form.vendedor_id
    ) {
      alert("Por favor llena todos los campos obligatorios");
      return;
    }

    // Armar objeto para enviar
    const dataToSend = {
      marca_id: Number(form.marca_id),
      modelo: form.modelo,
      anio: Number(form.anio),
      tipo: form.tipo || null,
      descripcion: form.descripcion || null,
      precio: form.precio.toString(), // enviar string para Decimal
      vendedor_id: Number(form.vendedor_id),
      disponible: Boolean(form.disponible),
      categorias: form.categorias || [],
    };

    if (vehiculoEdit) {
      onSubmit(vehiculoEdit.id, dataToSend);
    } else {
      onSubmit(dataToSend);
    }
    setForm(initialForm);
    clearEdit();
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white shadow-md rounded-xl p-6 max-w-md mx-auto mt-6 space-y-4"
    >
      <h2 className="text-xl font-semibold">
        {vehiculoEdit ? "Editar Vehículo" : "Registrar Vehículo"}
      </h2>

      <input
        type="number"
        name="marca_id"
        value={form.marca_id}
        onChange={handleChange}
        placeholder="Marca ID *"
        required
        className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <input
        name="modelo"
        value={form.modelo}
        onChange={handleChange}
        placeholder="Modelo *"
        required
        className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <input
        type="number"
        name="anio"
        value={form.anio}
        onChange={handleChange}
        placeholder="Año *"
        required
        className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <input
        name="tipo"
        value={form.tipo}
        onChange={handleChange}
        placeholder="Tipo"
        className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <textarea
        name="descripcion"
        value={form.descripcion}
        onChange={handleChange}
        placeholder="Descripción"
        className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <input
        name="precio"
        type="text"
        value={form.precio}
        onChange={handleChange}
        placeholder="Precio * (ej: 28000.00)"
        required
        className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <input
        type="number"
        name="vendedor_id"
        value={form.vendedor_id}
        onChange={handleChange}
        placeholder="Vendedor ID *"
        required
        className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <input
        type="text"
        name="categorias"
        value={form.categorias.join(",")}
        onChange={handleChange}
        placeholder="IDs de categorías, separados por coma"
        className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <label className="inline-flex items-center space-x-2">
        <input
          type="checkbox"
          name="disponible"
          checked={form.disponible}
          onChange={handleChange}
          className="form-checkbox"
        />
        <span>Disponible</span>
      </label>

      <div className="flex justify-end gap-2">
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
        >
          {vehiculoEdit ? "Actualizar" : "Crear"}
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
