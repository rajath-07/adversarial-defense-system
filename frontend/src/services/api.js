import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000"
});

export const predictImage = async (
    file,
    modelName,
    attackName
) => {

    const formData = new FormData();

    formData.append(
        "file",
        file
    );

    formData.append(
        "model_name",
        modelName
    );

    formData.append(
        "attack_name",
        attackName
    );

    const response = await API.post(
        "/predict",
        formData,
        {
            headers: {
                "Content-Type":
                    "multipart/form-data"
            }
        }
    );

    return response.data;
};