document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll(".router-link");

    // set active link based on current URL path
    const setActiveLink = () => {
        links.forEach(link => {
            // check if link's href matches the current URL path
            link.getAttribute("href") === window.location.pathname ? (
                link.classList.add("active"),
                link.setAttribute("aria-current", "page")
            ) : (
                link.classList.remove("active"),
                link.removeAttribute("aria-current")
            )
        });
    };

    // call setActiveLink on page load
    setActiveLink()

    // activate active state on click
    links.forEach(link => {
        link.addEventListener("click", () => {
            setActiveLink();
        });
    });
});