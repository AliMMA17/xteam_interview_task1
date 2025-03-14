import axios from "axios";
import { useEffect, useState } from "react";
import { getProducts } from "../api/api";

const Products = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Function to fetch products
    const fetchProducts = async () => {
        try {
            setLoading(true);  // Start loading when the request is made
            setError(null);    // Reset the error state before fetching again
            const data = await getProducts();
            setProducts(data);
        } catch (error) {
            console.error("Error fetching products:", error);
            setError("Failed to fetch products.");
            setProducts([]); // Clear products on error
        } finally {
            setLoading(false);  // Stop loading after request is completed
        }
    };

    // UseEffect to fetch products initially when the component mounts
    useEffect(() => {
        fetchProducts();
    }, []);

    // Button click handler to refresh products
    const handleRefresh = () => {
        fetchProducts();  // Call the function to fetch products
    };

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p className="error">{error}</p>;
    }

    return (
        <div className="products-container">
            <h1 className="title">All Products</h1>
            <button onClick={handleRefresh} className="refresh-button">
                Refresh Products
            </button>
            <ul className="products-list">
                {products.map((product) => (
                    <li key={product.id} className="product-item">
                        <h3>{product.name}</h3>
                        <p>Category: {product.category}</p>
                        <p>Price: ${product.price.toFixed(2)}</p>
                        <p>Rating: {product.rating} ⭐</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Products;
