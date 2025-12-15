(function () {
  function clearFormFields(formId) {
    if (!formId) return;

    var form =
      typeof formId === "string" ? document.getElementById(formId) : formId;
    if (!form) return;

    var selectors = [
      'input[type="text"]',
      'input[type="search"]',
      'input[type="email"]',
      'input[type="url"]',
      'input[type="tel"]',
      'input[type="number"]',
      'input[type="password"]',
      "input:not([type])",
      "textarea",
    ];

    form.querySelectorAll(selectors.join(",")).forEach(function (field) {
      field.value = "";
      if ("defaultValue" in field) {
        field.defaultValue = "";
      }
      field.dispatchEvent(new Event("input", { bubbles: true }));
      field.dispatchEvent(new Event("change", { bubbles: true }));
    });
  }

  window.clearFormFields = clearFormFields;
})();
