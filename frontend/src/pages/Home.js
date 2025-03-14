import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getUsers, createProduct } from "../api/api";
import "./Home.css"; // Import CSS

const Home = () => {
    const [users, setUsers] = useState([]);
    const [product, setProduct] = useState({ name: "", category: "", price: "", rating: "" });
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    useEffect(() => {
        getUsers().then(setUsers).catch(console.error);
    }, []);

    // Handle form input change
    const handleChange = (e) => {
        setProduct({ ...product, [e.target.name]: e.target.value });
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);
        try {
            const newProduct = await createProduct({
                ...product,
                price: parseFloat(product.price), // Ensure correct number format
                rating: parseFloat(product.rating),
            });
            setSuccess(`Product "${newProduct.name}" added successfully!`);
            setProduct({ name: "", category: "", price: "", rating: "" }); // Reset form
        } catch (error) {
            setError("Failed to add product. Please try again.");
        }
    };

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Users</h1>
            <ul>
                {users.map(user => (
                    <li key={user.id} className="p-2 border-b">
                        <Link to={`/user/${user.id}`} className="text-blue-500 hover:underline">
                            {user.name}
                        </Link>
                    </li>
                ))}
            </ul>

            {/* Add Product Form */}
            <div className="mt-6 p-4 border rounded">
                <h2 className="text-lg font-semibold mb-2">Add New Product</h2>
                {error && <p className="text-red-500">{error}</p>}
                {success && <p className="text-green-500">{success}</p>}
                <form onSubmit={handleSubmit} className="space-y-2">
                    <input
                        type="text"
                        name="name"
                        placeholder="Product Name"
                        value={product.name}
                        onChange={handleChange}
                        className="border p-2 w-full"
                        required
                    />
                    <input
                        type="text"
                        name="category"
                        placeholder="Category"
                        value={product.category}
                        onChange={handleChange}
                        className="border p-2 w-full"
                        required
                    />
                    <input
                        type="number"
                        name="price"
                        placeholder="Price"
                        value={product.price}
                        onChange={handleChange}
                        className="border p-2 w-full"
                        required
                    />
                    <input
                        type="number"
                        name="rating"
                        placeholder="Rating (1-5)"
                        value={product.rating}
                        onChange={handleChange}
                        className="border p-2 w-full"
                        required
                    />
                    <button
                        type="submit"
                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                    >
                        Add Product
                    </button>
                </form>
            </div>

            {/* "See All Products" Button */}
            <div className="mt-6">
                <Link to="/products" className="text-lg text-white bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded">
                    See All Products
                </Link>
            </div>
        </div>
    );
};

export default Home;
