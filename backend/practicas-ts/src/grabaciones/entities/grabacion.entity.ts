import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  CreateDateColumn,
  JoinColumn,
} from 'typeorm';
import { Usuario } from '../../usuarios/entities/usuario.entity';
import { Presentacion } from '../../presentaciones/entities/presentacion.entity';

@Entity('grabaciones')
export class Grabacion {
  @PrimaryGeneratedColumn()
  id_grabacion: number;

  @ManyToOne(() => Usuario, { eager: true })
  @JoinColumn({ name: 'id_usuario' })
  usuario: Usuario;

  @ManyToOne(() => Presentacion, { eager: true })
  @JoinColumn({ name: 'id_presentacion' })
  presentacion: Presentacion;

  @Column()
  archivo_audio: string;

  @CreateDateColumn({ type: 'timestamp' })
  fecha_grabacion: Date;
}
