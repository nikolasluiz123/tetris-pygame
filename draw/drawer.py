import time

import pygame
from OpenGL.GL import *
from pygame.locals import *

from config.configurator import Configurator


class Drawer:
    """
        Classe responsável por tratar tudo relacionado a movimentação
        dos objetos.
    """

    def __init__(self, configurator: Configurator):
        """
            Construtor para passagem dos parâmetros

            :param configurator: Objeto de configuração do jogo.
        """

        self.configurator = configurator
        self.clock = pygame.time.Clock()
        self.__locked_shapes = []

    def start_objects_movimentation(self):
        """
            Função principal que realiza a movimentação do objeto
            no eixo Y e permite que o usuário movimente-se no eixo
            X usando as setas.

            Além disso também trata o travamento (lock) do shape
            caso encoste na borda inferior da tela ou em outra peça
            que tenha sido posicionada.
        """

        for shape in self.configurator.shapes:
            while not shape.locked:
                glClear(GL_COLOR_BUFFER_BIT)

                self.execute_actions_on_events(shape)

                if self.configurator.shape_fits_game_matrix(shape):
                    self.update_object_positions(shape)
                else:
                    shape.locked = True
                    self.__locked_shapes.append(shape)
                    self.configurator.put_shape_in_game_matrix(shape)
                    self.configurator.delete_completed_matrix_lines()

                shape.draw()

                for locked_shape in self.__locked_shapes:
                    locked_shape.draw()

                pygame.display.flip()
                self.clock.tick(60)

    def execute_actions_on_events(self, shape):
        """
            Função responsável por tratar os eventos do jogo.

            Eventos:
                **QUIT** Quando o usuário fecha o jogo. Isso é necessário para que o processo do jogo não trave e que
                os recursos sejam liberados ao final do processo.

                **KEYDOWN** Quando o usuário aperta uma tecla. Pode ser usado para tratar a movimentação no eixo X do
                objeto.

                **KEYUP** Quando o usuário solta uma tecla. Pode ser usado para parar a movimentação no eixo X do
                objeto.
        """

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                self.move_object_on_x_axis(event, shape)
                self.rotate_shape(event, shape)
            elif event.type == KEYUP:
                self.stop_object_movimentation_on_x_axis(event, shape)

    def rotate_shape(self, event, shape):
        """
            Função responsável por iniciar a rotação do objeto.

            :param event: Evento realizado pelo usuário
            :param shape: Shape que será rotacionado
        """

        if event.key == K_UP:
            shape.rotate(clockwise=True)
        elif event.key == K_DOWN:
            shape.rotate(clockwise=False)

    def move_object_on_x_axis(self, event, shape):
        """
            Função responsável por mover o objeto no eixo X,
            tanto para esquerda como para a direita dependendo da tecla
            precionada.

            Se a tecla precisonada for a seta esquerda, a velocidade de movimentação
            do objeto precisa negativa.

            Se a tecla precionada for a seta direita, a velocidade de movimentação
            do objeto precisa ser positiva.

            :param shape: Shape que foi gerado
            :param event: Evento realizado pelo usuário
        """

        if event.key == K_LEFT:
            shape.speed_movimentation_x = -1
        elif event.key == K_RIGHT:
            shape.speed_movimentation_x = 1

    def stop_object_movimentation_on_x_axis(self, event, shape):
        """
            Função responsável por zerar a velocidade do objeto no eixo X
            caso seja necessário.

            :param shape: Shape que foi gerado
            :param event: Evento realizado pelo usuário
        """

        if event.key == K_LEFT or event.key == K_RIGHT:
            shape.speed_movimentation_x = 0

    def update_object_positions(self, shape):
        """
            Função responsável por atualizar a posição X e Y baseado na velocidade definida
            no Objeto. É usado um multiplicador para aumentar um pouco a velocidade, isso pode
            ser definido dinamicamente no futuro.

            :param shape: Shape que será movimentado
        """
        shape.position_x += shape.speed_movimentation_x * 2
        shape.position_y += shape.speed_movimentation_y * 2

        self.configurator.define_screen_limits_on_x_axis(shape)
