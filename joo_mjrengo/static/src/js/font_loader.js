/** @odoo-module **/

import { rpc } from "@web/core/network/rpc";

// Mapping between configuration keys and actual font-family names
const FONT_MAP = {
    ipamjm: "IPAmjMincho",
    dwpimincho: "DWPIMincho",
    dwpiexmincho: "DWPIexMincho",
};

/**
 * Fetch selected font from server and apply CSS.
 */
async function loadAndApplyFont() {
    try {
        const fontKey = await rpc("/joo_mjrengo/font");
        const fontFamily = FONT_MAP[fontKey] || null;

        if (!fontFamily) {
            console.warn(
                "[joo_mjrengo] Unknown font key received:",
                fontKey
            );
            return;
        }

        const css = `.joo-font { font-family: "${fontFamily}", serif !important; }`;

        const style = document.createElement("style");
        style.innerHTML = css;
        document.head.appendChild(style);

        console.debug("[joo_mjrengo] Applied font:", fontFamily);
    } catch (err) {
        console.error("[joo_mjrengo] Failed to load font configuration:", err);
    }
}

loadAndApplyFont();
