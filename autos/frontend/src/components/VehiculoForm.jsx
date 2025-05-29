import React, { useEffect, useState } from "react";
import styles from './VehiculoForm.module.css';

const initialForm = {
  id: null,
  marca_id: "",
  modelo: "",
  anio: "",
  tipo: "",
  descripcion: "",
  precio: "",
  vendedor_id: "",
  disponible: true,
  categorias: [], 
};

const VehiculoForm = ({ onSubmit, vehiculoEdit, clearEdit }) => {
  const [form, setForm] = useState(initialForm);

  useEffect(() => {
    if (vehiculoEdit) {
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

    const dataToSend = {
      marca_id: Number(form.marca_id),
      modelo: form.modelo,
      anio: Number(form.anio),
      tipo: form.tipo || null,
      descripcion: form.descripcion || null,
      precio: form.precio.toString(), 
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
      className={styles.input}
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
        className={styles.input}
      />

      <input
        name="modelo"
        value={form.modelo}
        onChange={handleChange}
        placeholder="Modelo *"
        required
        className={styles.input}
      />

      <input
        type="number"
        name="anio"
        value={form.anio}
        onChange={handleChange}
        placeholder="Año *"
        required
        className={styles.input}
      />

      <input
        name="tipo"
        value={form.tipo}
        onChange={handleChange}
        placeholder="Tipo"
        className={styles.input}
      />

      <textarea
        name="descripcion"
        value={form.descripcion}
        onChange={handleChange}
        placeholder="Descripción"
        className={styles.input}
      />

      <input
        name="precio"
        type="text"
        value={form.precio}
        onChange={handleChange}
        placeholder="Precio * (ej: 28000.00)"
        required
        className={styles.input}
      />

      <input
        type="number"
        name="vendedor_id"
        value={form.vendedor_id}
        onChange={handleChange}
        placeholder="Vendedor ID *"
        required
        className={styles.input}
      />

      <input
        type="text"
        name="categorias"
        value={form.categorias.join(",")}
        onChange={handleChange}
        placeholder="IDs de categorías, separados por coma"
        className={styles.input}
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
