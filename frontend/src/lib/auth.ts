const KEY = "isAdmin";

export const isAdmin = () => localStorage.getItem(KEY) === "true";
export const loginAsAdmin = () => localStorage.setItem(KEY, "true");
export const logout = () => localStorage.removeItem(KEY);
