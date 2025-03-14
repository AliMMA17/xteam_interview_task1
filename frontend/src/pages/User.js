import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getRecommendations } from "../api/api"; // ✅ Use the correct function name
import "./User.css"; // Import CSS

const User = () => {
    const { id } = useParams();
    const [products, setProducts] = useState([]);

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const data = await getRecommendations(id); // ✅ Correct function name
                setProducts(data);
            } catch (error) {
                console.error("Error fetching recommendations:", error);
            }
        };

        if (id) {
            fetchRecommendations();
        }
    }, [id]);

    return (
        <div className="user-container">
            <h2 className="user-title">Recommended Products</h2>
            <ul className="product-list">
                {products.map(product => (
                    <li key={product.id} className="product-item">
                        <h3>{product.name}</h3>
                        <p>Price: ${product.price.toFixed(2)}</p>
                        <p>Category: {product.category}</p>
                        <p>Rating: {product.rating} ⭐</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default User;
