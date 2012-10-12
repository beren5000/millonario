from django.db import models

class PerfilManager(models.Manager):


    def get_perfil(self,user_id):
        return self.get(user__id=user_id)

    def get_hijos(self, perfil_id):

        query="""SELECT  perfil_perfil.id,perfil_perfil.nombre,perfil_perfil.apellidos , IFNULL(sum(  ef.visitas )   , 0) clicks
        FROM

        inviter_contactsregister AS hijos
        LEFT OUTER JOIN  estadisticas_estadistica ee on ee.perfil_id=hijos.invite_profile_id
        LEFT OUTER JOIN  estadisticas_fechaxestadistica  ef on ef.estadistica_id=ee.id
        inner JOIN  perfil_perfil   on perfil_perfil.id=hijos.invite_profile_id
        WHERE hijos.user_profile_id=%s
        GROUP BY perfil_perfil.id   """

        return self.raw(query%perfil_id)
    
    def get_nietos(self, perfil_id):
        query="""SELECT  perfil_perfil.id, perfil_perfil.nombre, perfil_perfil.apellidos
                ,  IFNULL(sum(  ef.visitas )   , 0) clicks
                FROM inviter_contactsregister hijos, inviter_contactsregister nietos
                LEFT OUTER JOIN  estadisticas_estadistica ee on ee.perfil_id=nietos.invite_profile_id
                LEFT OUTER JOIN  estadisticas_fechaxestadistica  ef on ef.estadistica_id=ee.id
                INNER join  perfil_perfil on perfil_perfil.id =nietos.invite_profile_id
                WHERE hijos.user_profile_id=%s
                AND nietos.user_profile_id=hijos.invite_profile_id
                GROUP BY perfil_perfil.id
                """
        return self.raw(query%perfil_id)
        
class PerfilManagerOptimizado(PerfilManager):
    def get_query_set(self):        
        return super(PerfilManagerOptimizado, self).get_query_set().filter(perfil_completo=True)
