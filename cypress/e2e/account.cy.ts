import {login} from "../support/functions";

describe('template spec', () => {
  it(' should register user', () => {
    cy.visit('/register')
    cy.get('#id_username').type('testuser')
    cy.get('#id_email').type('testemail@mail.com')
    cy.get('#id_password').type('Silnehaslo1')
    cy.get('#id_password_confirm').type('Silnehaslo1')
    cy.get('input[value="Zarejestruj się"]').click();
    cy.wait(5000)
  })
    it('should login user', () => {
    cy.visit('login')
    cy.get('#id_username').type('testuser')
    cy.get('#id_password').type('Silnehaslo1')
    cy.get('input[value="Zaloguj się"]').click();
    cy.wait(5000)

  });

})