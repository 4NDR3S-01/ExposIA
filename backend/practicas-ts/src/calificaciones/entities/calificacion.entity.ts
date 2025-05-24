import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, JoinColumn } from 'typeorm';
import { Feedback } from '../feedbacks/feedback.entity';
import { Usuario } from '../../usuarios/entities/usuario.entity';

@Entity('calificaciones')
export class Calificacion {
  @PrimaryGeneratedColumn()
  id_calificacion: number;

  @ManyToOne(() => Feedback)
  @JoinColumn({ name: 'id_feedback' })
  feedback: Feedback;

  @ManyToOne(() => Usuario)
  @JoinColumn({ name: 'id_usuario' })
  usuario: Usuario;

  @Column()
  puntuacion: number;

  @Column({ nullable: true })
  observacion: string;

  @Column()
  fecha: Date;
}