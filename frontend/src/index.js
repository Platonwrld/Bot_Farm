import React from 'react';
import ReactDOM from 'react-dom/client';
import { HashRouter, Routes, Route } from "react-router-dom";

import LoginPage from "./pages/login";
import DashboardPage from "./pages/dashboard";
import AddAccountsPage from "./pages/add_accounts";
import AddProxiesPage from "./pages/add_proxies";
import AddTasksPage from "./pages/add_task";
import GetAccountsPage from "./pages/get_accounts";
import GetProxiesPage from "./pages/get_proxies";
import GetChannelsPage from "./pages/get_channels";
import GetTasksPage from "./pages/get_tasks";
import ChannelPage from "./pages/channel";
import Error404Page from "./pages/404";


import "./static/css/main.css";

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
    <HashRouter>
        <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<DashboardPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/add_accounts" element={<AddAccountsPage />} />
            <Route path="/add_proxies" element={<AddProxiesPage />} />
            <Route path="/add_task" element={<AddTasksPage />} />
            <Route path="/get_accounts" element={<GetAccountsPage />} />
            <Route path="/get_proxies" element={<GetProxiesPage />} />
            <Route path="/get_channels" element={<GetChannelsPage />} />
            <Route path="/get_tasks" element={<GetTasksPage />} />
            <Route path="/channel/:channel_id" element={<ChannelPage />} />
            <Route path="*" element={<Error404Page/>} />
        </Routes>
    </HashRouter>
);
