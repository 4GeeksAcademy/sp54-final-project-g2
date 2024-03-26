import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import injectContext from "./store/appContext";
// Import custom component
import ScrollToTop from "./component/scrollToTop.js";
import { BackendURL } from "./component/BackendURL.jsx";
import { Navbar } from "./component/Navbar.jsx";
import { Footer } from "./component/Footer.jsx";
// Import custom pages
import { Home } from "./pages/Home.jsx";
import { Demo } from "./pages/Demo.jsx";
import { Login } from "./pages/Login.jsx";
import { Register } from "./pages/Register.jsx";
import { Recipes } from "./pages/Recipes.jsx";
import { Previsions } from "./pages/Previsions.jsx";
import { DeliveryNotes } from "./pages/DeliveryNotes.jsx";
import { ManufacturingOrders } from "./pages/ManufacturingOrders.jsx";
import { Single } from "./pages/Single.jsx";
import { References } from "./pages/References.jsx";
import { Suppliers } from "./pages/Suppliers.jsx";



// Create your first component
const Layout = () => {
    // The basename is used when your project is published in a subdirectory and not in the root of the domain
    // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
    const basename = process.env.BASENAME || "";
    if (!process.env.BACKEND_URL || process.env.BACKEND_URL == "") return <BackendURL/ >;

    return (
        <div>
            <BrowserRouter basename={basename}>
                <ScrollToTop>
                    <Navbar />
                    <Routes>
                        <Route element={<Login />} path="/login" />
                        <Route element={<Home />} path="/" />
                        <Route element={<Demo />} path="/demo" />
                        <Route element={<Single />} path="/single/:theid" />
                        <Route element={<h1>Not found!</h1>} />
                        <Route element={<Register />} path="/register" />
                        <Route element={<Recipes />} path="/recipes" />
                        <Route element={<Previsions />} path="/previsions" />
                        <Route element={<DeliveryNotes />} path="/delivery-notes" />
                        <Route element={<ManufacturingOrders />} path="/manufacturing-orders" />
                        <Route element={<References />} path="/references" />
                        <Route element={<Suppliers />} path="/suppliers" />
                    </Routes>
                    <Footer />
                </ScrollToTop>
            </BrowserRouter>
        </div>
    );
};

export default injectContext(Layout);
