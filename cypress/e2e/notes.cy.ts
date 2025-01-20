import {login} from "../support/functions";

describe('template spec', () => {
  beforeEach(() => {
    login()
  })


  it('should add new course', () => {
    cy.get('.menu').contains('Kursy').click()
    cy.get('.btn-add-note').contains('Dodaj kurs').click()
    cy.get('#id_name').type('Zarządzanie projektem informatycznym')
    cy.get('#id_university').select('pk')
    cy.get('.btn-submit').contains('Zapisz').click();
    cy.wait(5000)
  });

  it('should add new note to course', () => {
    cy.get('.user-button').click();
    cy.get('.settings-btn').contains('Zarządzaj notatkami').click();
    cy.get('.btn-add-note').click()
    cy.get('#id_title').type('Notatka przed egzaminem');
    cy.get('#id_body').type('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ' +
        'incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut' +
        ' aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla ' +
        'pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');
    cy.get('#id_university').select('pk');
    cy.get('#id_course').then((courseSelect) => {
      expect(courseSelect).to.exist;
      cy.get('#id_course').select('Zarządzanie projektem informatycznym');
    });
    cy.get('button[type="submit"]').click();
    cy.url().should('include', 'notatka-przed-egzaminem')
  });

  it('should search for notes and courses', () => {
    cy.get('.menu').contains('Notatki').click()
    cy.get('.search-input').type('egzamin')
    cy.get('.search-button').click()
    cy.wait(5000)
    cy.get('.menu').contains('Notatki').click()
    cy.get('.search-input').type('projekt')
    cy.get('.search-button').click()
    cy.wait(5000)

  });

  it('should add notes to favourites', () => {
    let noteTitle: string = '';
    cy.get('.menu').contains('Notatki').click()
    cy.get('.search-input').type('egzamin')
    cy.get('.notes-container .note-item').eq(0).find('.btn-add-favorite').click();
    cy.get('.notes-container .note-item').first().find('.note-title').invoke("text").then((title:any) =>{
      noteTitle = title.trim()
    });
    cy.get('.notes-container .note-item').eq(0).find('.btn-add-favorite').should('not.exist');
    cy.get('.notes-container .note-item').eq(0).find('.btn-remove-favorite').should('exist');
    cy.get('.menu').contains('Dashboard').click()
    cy.get('.notes-container .note-item').first().find('.note-title').invoke("text").then((title:any) =>{
      expect(noteTitle).to.eq(title.trim())
      cy.wait(5000)
    });
  });

  it('should block editing and deleting other user notes', () => {
    cy.get('.menu').contains('Notatki').click()
    cy.get('.notes-container .note-item').last().find('.note-title').click()
    cy.get('.edit-link').click()
    cy.get('.form-container').should("contain", 'Hej Kolego, nie powinno cię tu być.')
    cy.wait(5000)
    cy.get('.btn-primary').click()
    cy.get('.notes-container .note-item').last().find('.note-title').click()
    cy.get('.delete-link').click()
    cy.get('.form-container').should("contain", 'Hej Kolego, nie powinno cię tu być.')
    cy.wait(5000)
  });
  it('should edit notes', () => {
  cy.get('.user-button').click();
  cy.get('.settings-btn').contains('Zarządzaj notatkami').click();
  cy.get('.notes-container .note-item').first().find('a[title="Edytuj"]').click();
  cy.get('#id_title').type(' Chochlik');
  cy.wait(2000)
  cy.get('.btn-submit').click();
  cy.get('.note-title').should('contain', 'Chochlik');
  cy.wait(5000)
  });

  it('should delete notes', () => {
    cy.get('.user-button').click();
    cy.get('.settings-btn').contains('Zarządzaj notatkami').click();
    cy.get('.notes-container .note-item').first().find('a[title="Usuń"]').click();
    cy.get('.delete-btn').click()
    cy.get('.user-button').click();
    cy.get('.settings-btn').contains('Zarządzaj notatkami').click();
    cy.get('.notes-container .note-item').first().find('.note-title').should('not.contain', 'Notatka przed egzaminem')
    cy.wait(5000);
  });

})