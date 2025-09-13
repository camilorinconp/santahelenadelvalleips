from uuid import UUID

from .atencion_model import Atencion
from .medico_model import Medico
from .paciente_model import Paciente
from .intervencion_colectiva_model import IntervencionColectiva
from .atencion_primera_infancia_model import AtencionPrimeraInfancia
from .atencion_materno_perinatal_model import AtencionMaternoPerinatal
from .tamizaje_oncologico_model import TamizajeOncologico
from .control_cronicidad_model import ControlCronicidad, ControlCronicidadPolimorfica # Añadido ControlCronicidadPolimorfica
from .control_hipertension_model import ControlHipertensionDetalles
from .control_diabetes_model import ControlDiabetesDetalles
from .control_erc_model import ControlERCDetalles
from .control_dislipidemia_model import ControlDislipidemiaDetalles

# Modelos transversales con nomenclatura descriptiva en español para RAG/IA
from .entorno_model import (
    TipoEntornoSaludPublica,
    NivelComplejidadIntervencionEntorno,
    EstadoActivacionEntorno,
    ModeloEntornoSaludPublicaIntegralCompleto,
    ModeloEntornoSaludPublicaCrear,
    ModeloEntornoSaludPublicaActualizar,
    ModeloEntornoSaludPublicaRespuesta,
    ModeloListaEntornosSaludPublica,
    ModeloFiltrosEntornoSaludPublica,
    ModeloEstadisticasEntornoSaludPublica
)
from .familia_model import (
    TipoEstructuraFamiliarIntegral,
    CicloVitalFamiliarEvolutivo,
    ModeloFamiliaIntegralSaludPublica,
    RelacionIntegranteFamiliaCompleta,
    IntervencionSaludFamiliarIntegral
)
from .atencion_integral_model import (
    TipoAbordajeAtencionIntegralSalud,
    ModalidadAtencionIntegral,
    NivelComplejidadAtencionIntegral,
    EstadoAtencionIntegral,
    ModeloAtencionIntegralTransversalSaludCompleto,
    ModeloAtencionIntegralTransversalSaludCrear,
    ModeloAtencionIntegralTransversalSaludRespuesta,
    ModeloAtencionIntegralTransversalSaludActualizar
)
