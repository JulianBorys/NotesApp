export function login() {
    cy.visit('/')
    cy.get('#id_username').type('testuser')
    cy.get('#id_password').type('Silnehaslo1')
    cy.get('input[value="Zaloguj się"]').click();
}